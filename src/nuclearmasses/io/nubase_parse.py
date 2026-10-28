"""
The nubase_parse module defines the ``NUBASEParser`` class. This class contains the logic required to sort and organise
the inputs to :meth:`pandas.read_fwf` dependent on the year of the file. Once parsed, known typos and inconsistencies
are cleaned from the resultant dataframe.
"""

from dataclasses import dataclass
from decimal import Decimal
import re

import pandas as pd

from nuclearmasses.io.nubase_file import NUBASEFile, NUBASELayout
from nuclearmasses.utils.dataframe_utils import calculate_relative_error, read_fwf, strip_char_from_string_columns
from nuclearmasses.utils.periodic import get_symbol
from nuclearmasses.utils.type_defs import DataInput
from nuclearmasses.utils.units import unit_to_seconds


@dataclass(frozen=True, kw_only=True)
class DecayMeasurement:
    """
    Storage class for decay mode details
    """

    decay_type: str
    operator: str | None
    percentage: Decimal | None
    error: Decimal | None = None
    upper_error: Decimal | None = None
    lower_error: Decimal | None = None
    annotation: str | None = None
    status: str = "reported"
    raw: str | None = None


# Depending on how you are feeling, the next few lines are either beautifully elegant or a chaotic mess.
# Decimal or scientific-notation number, e.g. 100, .5, 10.0e-13.
UNSIGNED_NUM = r"(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"

# NUM allows a leading sign; ERR_NUM does not, e.g. -0.13 vs. 0.7e-3.
NUM = rf"[+-]?{UNSIGNED_NUM}"
ERR_NUM = UNSIGNED_NUM

# We are attempting to represent all forms of decay string in a single regex,
# capturing the parts we are interested into capture groups to access after the match.
DECAY_PATTERN = re.compile(
    rf"^(?P<decay_type>[A-Za-z0-9][A-Za-z0-9_+()\-]*)"
    rf"(?P<operator>>=|<=|=<|=>|>|<|=|~)"
    rf"(?P<value>{NUM})"
    rf"(?:"
    rf"\s+\+(?P<upper_error>{ERR_NUM})"
    rf"-(?P<lower_error>{ERR_NUM})"
    rf"|\s+(?P<error>{ERR_NUM})"
    rf")?"
    rf"\s*(?P<annotation>\[[^\]]*\])?"
    rf"\?*$"
)


class NUBASEParser:
    """
    Parse the NUBASE file, doing the necessary preparations and clean up of data.

    There are some quirks to the format used in the file. It's based on fixed-width format, but deviates in various
    various places so additional work is required once the file is parsed.

    Parameters
    ----------
    filename : DataInput
        The file-like object to parse.
    year : int
        The published year of the data file.

    Attributes
    ----------
    filename : DataInput
        The file-like object to parse.
    year : int
        The published year of the data file.
    layout : NUBASELayout
        A storage class containing details of parameters and their location in the line.
    unit_replacements : dict[str, str]
        A dictionary used to tidy up time units from NUBASE format to one the module recognises.
    column_limits : list[tuple[int|None, int|None]]
        The start and end positions of all parameters as a list of tuples that can be passed to :meth:`pandas.read_fwf`.
    """

    def __init__(self, filename: DataInput, year: int):
        self.filename: DataInput = filename
        self.year: int = year

        self.layout: NUBASELayout = NUBASEFile(year=year).layout
        self.column_limits: list[tuple[int | None, int | None]] = [
            (getattr(self.layout, start), getattr(self.layout, end)) for _, start, end in self.layout.positions
        ]

        if year > 2003:
            self.column_limits.insert(-1, (self.layout.START_DiscoveryYear, self.layout.END_DiscoveryYear))

    def _column_names(self) -> list[str]:
        """
        Set the column name depending on the year.

        Returns
        -------
        list[str]
            An ordered list of the columns that exist in the file.
        """
        col_names = self.layout.columns

        if self.year > 2003:
            col_names.insert(-1, "DiscoveryYear")

        return col_names

    def _data_types(self) -> dict[str, str]:
        """
        Set the column data types depending on the year.

        Returns
        -------
        dict[str, str]
            A dictionary of the columns that exist and their data type
        """
        data_types = {
            "Symbol": "string",
            "A": "Int64",
            "Z": "Int64",
            "N": "Int64",
            "Experimental": "boolean",
            "NUBASEMassExcess": "Float64",
            "NUBASEMassExcessError": "Float64",
            "NUBASERelativeError": "Float64",
            "HalfLifeValue": "Float64",
            "HalfLifeUnit": "string",
            "HalfLifeError": "Float64",
            "HalfLifeSeconds": "Float64",
            "HalfLifeSecondsError": "Float64",
            "Spin": "string",
            "DiscoveryYear": "Int64",
            "DecayModes": "string",
            "DataSource": "Int64",
            # We will need these one day
            # "State": "Int64",
            # "IsomerEnergy": "Float64",
            # "IsomerEnergyError": "Float64",
        }

        # The discovery year was added after 2003, and I assume it will be there in the future, so we will set up
        # as if it is always present and delete for the first two tables.
        if self.year <= 2003:
            data_types.pop("DiscoveryYear")

        return data_types

    def _na_values(self) -> dict:
        """
        Set the columns that have empty fields that should be NaN'd depending on the year.

        Returns
        -------
        dict[str, list[str]]
            A dictionary of the columns that will have values that should be interpreted as NaN.
        """
        na_values = {
            "State": [""],
            "NUBASEMassExcess": [""],
            "NUBASEMassExcessError": [""],
            "HalfLifeValue": [""],
            "HalfLifeUnit": [""],
            "HalfLifeError": [""],
            "DecayModes": [""],
            "Spin": [""],
        }

        if self.year == 1995:
            na_values["Spin"] = [""]
        else:
            na_values["HalfLifeValue"] = ["", "p-unst", "p-unst#"]
            na_values["DiscoveryYear"] = [""]

        return na_values

    def parse_single_decay_string(self, text: str) -> DecayMeasurement | None:
        """
        Parse a single decay mode into a DecayMeasurement storage class

        There is a large amount of detail given in a single string. To avoid the loss of any of this informations, we
        use a custom storage class that has each piece of information extracted into attributes. The raw string is also
        saved in case there was an issue with the parse.

        Parameters
        ----------
        text : str
            The string containing the decay properties.

        Returns
        -------
        DecayMeasurement
            An instance of the DecayMeasurement storage class with all the necessary data.

        """
        if not text:
            return None

        if text.endswith("?"):
            if text.endswith("=?"):
                return DecayMeasurement(
                    decay_type=text[:-2],
                    operator="=",
                    percentage=None,
                    status="Observed but not yet quantified",
                    raw=text,
                )
            if "=" not in text:
                return DecayMeasurement(
                    decay_type=text[:-1],
                    operator=None,
                    percentage=None,
                    status="Energetically Allowed",
                    raw=text,
                )
        elif text == "...":
            return DecayMeasurement(
                decay_type="Continued",
                operator="=",
                percentage=None,
                status="unknown",
                raw=text,
            )

        match = DECAY_PATTERN.fullmatch(text)

        if not match:
            print(f"Unrecognised decay string: {text!r}")
            return DecayMeasurement(
                decay_type="Unparsed",
                operator="=",
                percentage=None,
                status="unknown",
                raw=text,
            )

        (decay_type, operator, val_str, upper_err_str, lower_err_str, err_str, annotation) = match.groups()

        value = Decimal(val_str)
        # Cast to silence ty checker
        exponent = int(value.as_tuple().exponent)

        # Scale uncertainties using the final displayed digit of the value.
        # The "b" in scaleb usually means binary and x.scaleb(y) == x * 2**y. However, as this python implementation is
        # within the decimal library, it is a power of 10, not 2, so works for what we want it to do.
        error = Decimal(err_str).scaleb(exponent) if err_str is not None else None
        upper_error = Decimal(upper_err_str).scaleb(exponent) if upper_err_str is not None else None
        lower_error = Decimal(lower_err_str).scaleb(exponent) if lower_err_str is not None else None

        # Strip square brackets
        if annotation is not None:
            annotation = annotation[1:-1]

        return DecayMeasurement(
            decay_type=decay_type,
            operator=operator,
            percentage=value,
            error=error,
            upper_error=upper_error,
            lower_error=lower_error,
            annotation=annotation,
            raw=text,
        )

    def parse_decay_modes(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        """
        Parse the raw string with all decay modes

        Parameters
        ----------
        raw_df : pandas.DataFrame
            The dataframe to use to convert raw decay strings into DecayMeasurements.

        Returns
        -------
        pandas.DataFrame
            The updated dataframe with new columns containing decay data.
        """
        # Start with some bookkeeping to fix likely typos
        # 1997 231Pa
        # Values is: "23F=10.0e-13 +5.0--0.7", assume single '-' for asymmetric errors to match other instances
        # (see discussion elsewhere as to why this relates to the 1995 table)
        if self.year == 1995:
            Pa231 = (raw_df["A"] == 231) & (raw_df["Z"] == 91)
            raw_df.loc[Pa231, "DecayModes"] = raw_df.loc[Pa231, "DecayModes"].str.replace("--", "-", regex=False)

        # 2012 198Au
        # Decay mode is recorded as '-=100', other years have it as "B-=100"
        if self.year == 2012:
            Au198 = (raw_df["A"] == 198) & (raw_df["Z"] == 79)
            raw_df.loc[Au198, "DecayModes"] = "B-=100"

        # 2012 & 2016 142Gd
        # Decay string is ',' separated rather than ';'
        if self.year == 2012 or self.year == 2016:
            Gd142 = (raw_df["A"] == 142) & (raw_df["Z"] == 64)
            raw_df.loc[Gd142, "DecayModes"] = raw_df.loc[Gd142, "DecayModes"].str.replace(",", ";", regex=False)

        # Replacements for when letters and characters have been used instead of symbols
        symbol_replacements = {
            r" GE ": ">=",
            r" LE ": "<=",
            r" \?": "?",
        }

        cleaned_series = raw_df["DecayModes"].str.replace(symbol_replacements, regex=True)

        parsed_results: list = []
        for val in cleaned_series.to_numpy():
            if val is None:
                parsed_results.append(pd.NA)
            else:
                # Clean, split, and immediately parse every item in a single pass
                parsed_results.append([self.parse_single_decay_string(item.strip()) for item in val.split(";")])

        raw_df["ParsedDecays"] = parsed_results

        return raw_df

    def parse_half_life(self, raw_df) -> pd.DataFrame:
        """
        Create additional half-life columns with values in seconds

        The half-life is stored as a human readable value, e.g. 2ms, 4Gyr, 5mins. This is fine to read but not to do
        any type of sorting or algorithm. Convert to the SI unit of seconds, but don't overwrite original columns.

        We do carry out some cleaning of the original columns by removing symbols and letters where we know they are
        numerical values.

        Parameters
        ----------
        raw_df : pandas.DataFrame
            The dataframe to use to convert raw half-life records into values in seconds.

        Returns
        -------
        pandas.DataFrame
            The updated dataframe with new columns containing half-life values in seconds.
        """
        raw_df["HalfLifeValue"] = raw_df["HalfLifeValue"].astype("string")
        raw_df["HalfLifeError"] = raw_df["HalfLifeError"].astype("string")

        # Convert stable isotopes into ones with enormous lifetimes with zero error so we can cast
        mask = raw_df["HalfLifeValue"] == "stbl"
        raw_df.loc[mask, ["HalfLifeValue", "HalfLifeUnit", "HalfLifeError"]] = ("99.99", "Zyr", "0.0")

        if self.year == 2016:
            # the half-life related columns are misaligned for 92Br in 2016
            mask = (raw_df.A == 92) & (raw_df.Z == 35)
            raw_df.loc[mask, ["HalfLifeValue", "HalfLifeUnit", "HalfLifeError"]] = ("0.314", "s", "0.016")

        raw_df["HalfLifeValue"] = pd.to_numeric(
            raw_df["HalfLifeValue"].replace(r"[<>?~]", "", regex=True), errors="coerce"
        )
        # We'll be lazy here and remove any characters in this column. Future us will parse this properly
        raw_df["HalfLifeError"] = pd.to_numeric(
            raw_df["HalfLifeError"].replace(r"[<>?~a-z]", "", regex=True), errors="coerce"
        )

        # Use the 3 half-life columns to create 2 new columns with units of seconds
        # Pre-compute unit -> second conversion
        unit_map = raw_df["HalfLifeUnit"].map(unit_to_seconds)

        raw_df["HalfLifeSeconds"] = raw_df["HalfLifeValue"] * unit_map
        raw_df["HalfLifeSecondsError"] = raw_df["HalfLifeError"] * unit_map

        return raw_df

    def parse_state(self, raw_df) -> pd.DataFrame:
        """
        Interpret the state of the isotope

        Currently we are only interested in ground states so drop any other row that is not that.
        In the future we will care about isomers.

        Parameters
        ----------
        raw_df : pandas.DataFrame
            The raw dataframe with all states of isotopes in.

        Returns
        -------
        pandas.DataFrame
            The updated dataframe containing only ground state data
        """
        # Ignore anything this is not the ground state
        raw_df = raw_df[raw_df["State"] == 0]
        # As 'State' is now necessarily 0 and the Isomer columns are empty, drop them.
        raw_df = raw_df.drop(columns=["State", "IsomerEnergy", "IsomerEnergyError"])

        return raw_df

    def read_file(self) -> pd.DataFrame:
        """
        Read the file-like object ``self.filename`` into a dataframe

        The ``NUBASEFile`` and other functions in this class have hopefully sanitized the column names, data types and
        locations of the date so we can now make the generic call to parse the file.

        Returns
        -------
        pandas.DataFrame
            A dataframe containing the parsed and organised contents of the NUBASE data file
        """
        df = read_fwf(
            self.filename,
            colspecs=self.column_limits,
            names=self._column_names(),
            na_values=self._na_values(),
            keep_default_na=False,
            on_bad_lines="warn",
            skiprows=self.layout.HEADER,
            skipfooter=self.layout.FOOTER,
        )

        df = self.parse_state(df)

        # We use the NUBASE data to define whether or not an isotope is experimentally measured,
        df["Experimental"] = ~df["NUBASEMassExcess"].astype("string").str.contains("#", na=False)
        # Once we have used the '#' to determine if it's experimental or not, we can remove all instances of it
        df = strip_char_from_string_columns(df, "#")

        df = self.parse_half_life(df)
        df = calculate_relative_error(df, "NUBASE")
        df = self.parse_decay_modes(df)

        df["TableYear"] = self.year
        df["N"] = pd.to_numeric(df["A"]) - pd.to_numeric(df["Z"])
        df["Symbol"] = pd.to_numeric(df["Z"]).map(get_symbol)
        df["DataSource"] = 0

        return df.astype(self._data_types())
