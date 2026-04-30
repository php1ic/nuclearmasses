"""
The nubase_parse module defines the ``NUBASEParser`` class. This class contains the logic required to sort and organise
the inputs to :meth:`pandas.read_fwf` dependent on the year of the file. Once parsed, known typos and inconsistencies
are cleaned from the resultant dataframe.
"""

import typing

import pandas as pd

from nuclearmasses.io.nubase_file import NUBASEFile
from nuclearmasses.utils.converter import Converter, DataInput


class NUBASEParser(NUBASEFile, Converter):
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
    unit_replacements : dict[str, str]
        A dictionary used to tidy up time units from NUBASE format to one the module recognises.
    """

    def __init__(self, filename: DataInput, year: int):
        super().__init__(year=year)
        self.filename: DataInput = filename
        self.year: int = year
        self.unit_replacements: dict[str, str] = {
            r"y$": "yr",
            r"^m$": "min",
        }

    def _column_names(self) -> list[str]:
        """
        Set the column name depending on the year.

        Returns
        -------
        list[str]
            An ordered list of the columns that exist in the file.
        """
        col_names = [
            "A",
            "Z",
            "State",
            "NUBASEMassExcess",
            "NUBASEMassExcessError",
            "IsomerEnergy",
            "IsomerEnergyError",
            "HalfLifeValue",
            "HalfLifeUnit",
            "HalfLifeError",
            "Spin",
            "DiscoveryYear",
            "DecayModes",
        ]

        # The discovery year was added after 2003, and I assume it will be there in the future, so we will set up
        # as if it is always present and delete for the first two tables.
        if self.year == 1995 or self.year == 2003:
            col_names.remove("DiscoveryYear")

        return col_names

    def _data_types(self) -> dict:
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
            # "State": "Int64",
            "NUBASEMassExcess": "float64",
            "NUBASEMassExcessError": "float64",
            # "IsomerEnergy": "float64",
            # "IsomerEnergyError": "float64",
            "HalfLifeValue": "float64",
            "HalfLifeUnit": "string",
            "HalfLifeError": "float64",
            "HalfLifeSeconds": "float64",
            "HalfLifeErrorSeconds": "float64",
            "Spin": "string",
            "DiscoveryYear": "Int64",
            "DecayModes": "string",
            "DataSource": "Int64",
        }

        # The discovery year was added after 2003, and I assume it will be there in the future, so we will set up
        # as if it is always present and delete for the first two tables.
        if self.year == 1995 or self.year == 2003:
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
        }

        if self.year == 1995:
            na_values["Spin"] = [""]
        else:
            na_values["HalfLifeValue"] = ["", "p-unst", "p-unst#"]
            na_values["DiscoveryYear"] = [""]

        return na_values

    def parse_half_life(self, raw_df) -> pd.DataFrame:
        """
        Create additional half-life columns with values in seconds

        The half-life is stored as a human readable value, e.g. 2ms, 4Gyr, 5mins. This is fine to read but not to do
        any type of sorting or algorithm. Convert to the SI unit of seconds, but don't overwrite original columns.

        Parameters
        ----------
        raw_df : pandas.DataFrame
            The dataframe to use to convert raw half-life records into values in seconds.

        Returns
        -------
        pandas.DataFrame
            The updated dataframe with new columns containing half-life values in seconds.
        """
        # Convert stable isotopes into ones with enormous lifetimes with zero error so we can cast
        raw_df["HalfLifeValue"] = raw_df["HalfLifeValue"].astype("object")
        raw_df["HalfLifeError"] = raw_df["HalfLifeError"].astype("object")

        mask = raw_df["HalfLifeValue"] == "stbl"
        raw_df.loc[mask, ["HalfLifeValue", "HalfLifeUnit", "HalfLifeError"]] = (99.99, "Zyr", 0.0)

        if self.year == 2016:
            # the half-life related columns are misaligned for 92Br in 2016
            mask = (raw_df.A == 92) & (raw_df.Z == 35)
            raw_df.loc[mask, ["HalfLifeValue", "HalfLifeUnit", "HalfLifeError"]] = (0.314, "s", 0.016)

        raw_df["HalfLifeValue"] = raw_df["HalfLifeValue"].astype("string").str.replace(r"[<>?~]", "", regex=True)
        # We'll be lazy here and remove any characters in this column. Future us will parse this properly
        raw_df["HalfLifeError"] = raw_df["HalfLifeError"].astype("string").str.replace(r"[<>?~a-z]", "", regex=True)

        # Use the 3 half-life columns to create 2 new columns with units of seconds
        raw_df["HalfLifeUnit"] = raw_df["HalfLifeUnit"].astype("string")
        # Bookkeeping: Tidy up know unusual units, i.e. y for years and m for minutes
        for pattern, replacement in self.unit_replacements.items():
            raw_df["HalfLifeUnit"] = raw_df["HalfLifeUnit"].str.replace(pattern, replacement, regex=True)

        # Ensure numeric values
        for col in ["HalfLifeValue", "HalfLifeError"]:
            raw_df[col] = pd.to_numeric(raw_df[col], errors="coerce")

        # Pre-compute unit -> second conversion
        unit_map = raw_df["HalfLifeUnit"].map(self.unit_to_seconds)

        raw_df["HalfLifeSeconds"] = raw_df["HalfLifeValue"] * unit_map
        raw_df["HalfLifeErrorSeconds"] = raw_df["HalfLifeError"] * unit_map

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

    def calculate_relative_error(self, raw_df) -> pd.DataFrame:
        """
        Calculate the relative error of the mass excess.

        12C has a 0.0 +/- 0.0 mass excess by definition, so relative error is 0.0. The division by zero will put a NaN
        value in the column for 12C so we will manually correct and set to 0.0.

        Parameters
        ----------
        raw_df : pandas.DataFrame
            The raw dataframe upon which we will act.

        Returns
        -------
        pandas.DataFrame
            The updated dataframe with a new relative mass excess column.
        """
        raw_df["NUBASERelativeError"] = abs(
            raw_df["NUBASEMassExcessError"].astype(float) / raw_df["NUBASEMassExcess"].astype(float)
        )
        raw_df.loc[(raw_df.Z == 6) & (raw_df.A == 12), "NUBASERelativeError"] = 0.0

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
        df = Converter.read_fwf(
            self.filename,
            colspecs=typing.cast(typing.Sequence[tuple[int, int]], self.column_limits),  # appease mypy
            names=self._column_names(),
            na_values=self._na_values(),
            keep_default_na=False,
            on_bad_lines="warn",
            skiprows=self.HEADER,
            skipfooter=self.FOOTER,
        )

        df = self.parse_state(df)

        # We use the NUBASE data to define whether or not an isotope is experimentally measured,
        df["Experimental"] = ~df["NUBASEMassExcess"].astype("string").str.contains("#", na=False)
        # Once we have used the '#' to determine if it's experimental or not, we can remove all instances of it
        df = self.strip_char_from_string_columns(df, "#")

        df = self.parse_half_life(df)
        df = self.calculate_relative_error(df)

        if self.year == 2012:
            # 198Au has a typo in it's decay mode in the 2012 table. It is recorded as '-'
            df.loc[(df.A == 198) & (df.Z == 79), "DecayModes"] = "B-"

        df["TableYear"] = self.year
        df["N"] = pd.to_numeric(df["A"]) - pd.to_numeric(df["Z"])
        df["Symbol"] = pd.to_numeric(df["Z"]).map(self.get_symbol)
        df["DataSource"] = 0

        return df.astype(self._data_types())
