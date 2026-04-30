"""
The ame_mass_parse module defines the ``AMEMassParser`` class. This class contains the logic required to sort and
organise the inputs to :meth:`pandas.read_fwf` dependent on the year of the file. Once parsed, known typos and
inconsistencies are cleaned from the resultant dataframe.
"""

import pandas as pd

from nuclearmasses.io.ame_mass_file import AMEMassFile
from nuclearmasses.utils.converter import Converter, DataInput


class AMEMassParser(AMEMassFile, Converter):
    """
    Parse the AME mass file, doing the necessary preparation and clean ups of data.

    There are some quirks to the format used in the file. It's based on fixed-width format, but deviates in various
    places so additional work is required once the file is parsed.

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
    """

    def __init__(self, filename: DataInput, year: int):
        super().__init__(year=year)
        self.filename: DataInput = filename
        self.year: int = year

    def _column_names(self) -> list[str]:
        """
        Set the column name depending on the year.

        Returns
        -------
        list[str]
            An ordered list of the columns that exist in the file.
        """
        return [
            "Z",
            "A",
            "AMEMassExcess",
            "AMEMassExcessError",
            "BindingEnergyPerA",
            "BindingEnergyPerAError",
            "BetaDecayEnergy",
            "BetaDecayEnergyError",
            "AtomicNumber",
            "AtomicMass",
            "AtomicMassError",
        ]

    def _data_types(self) -> dict:
        """
        Set the column data types depending on the year.

        Returns
        -------
        dict[str, str]
            A dictionary of the columns that exist and their data type
        """
        return {
            "TableYear": "Int64",
            "Symbol": "string",
            "N": "Int64",
            "Z": "Int64",
            "A": "Int64",
            "AMEMassExcess": "float64",
            "AMEMassExcessError": "float64",
            "BindingEnergyPerA": "float64",
            "BindingEnergyPerAError": "float64",
            "BetaDecayEnergy": "float64",
            "BetaDecayEnergyError": "float64",
            "AtomicMass": "float64",
            "AtomicMassError": "float64",
            "DataSource": "Int64",
        }

    def _na_values(self) -> dict:
        """
        Set the columns that have empty fields that should be NaN'd depending on the year.

        Returns
        -------
        dict[str, list[str]]
            A dictionary of the columns that will have values that should be interpreted as NaN.
        """
        na_vals = {
            "A": [""],
            "BetaDecayEnergy": ["", "*"],
            "BetaDecayEnergyError": ["", "*"],
        }

        if self.year != 1983:
            na_vals.pop("A")

        return na_vals

    def read_file(self) -> pd.DataFrame:
        """
        Read the file-like object ``self.filename`` into a dataframe

        The ``AMEMassFile`` and other functions in this class have hopefully sanitized the column names, data types and
        locations of the date so we can now make the generic call to parse the file.

        Returns
        -------
        pandas.DataFrame
            A dataframe containing the parsed and organised contents of the AME mass data file
        """
        df = Converter.read_fwf(
            self.filename,
            colspecs=self.column_limits,
            names=self._column_names(),
            na_values=self._na_values(),
            keep_default_na=False,
            on_bad_lines="warn",
            skiprows=self.HEADER,
            skipfooter=self.FOOTER,
        )
        # We use the NUBASE data to define whether or not an isotope is experimentally measured,
        # so for this data we'll just drop any and all '#' characters
        df = self.strip_char_from_string_columns(df, "#")

        if self.year == 1983:
            # The column headers and units are repeated in the 1983 table
            df = df[(df["A"] != "A") & (~df["AMEMassExcess"].astype("string").str.contains("keV", na=False))]
            # The A value is not in the column if it doesn't change so we need to fill down
            df["A"] = df["A"].ffill()
            # Isomeric states are sometimes included in this version of the file
            # For each row in the dataframe, if the previous row has equal A and Z, drop the current row
            df = df[~((df["A"] == df["A"].shift()) & (df["Z"] == df["Z"].shift()))]

        if self.year == 1983 or self.year == 1993 or self.year == 1995:
            df["BindingEnergyPerA"] = df["BindingEnergyPerA"].astype(float) / df["A"].astype(float)
            df["BindingEnergyPerAError"] = df["BindingEnergyPerAError"].astype(float) / df["A"].astype(float)

        # Combine the two columns to create the atomic mass then drop the redundant column
        # Pandas is happy to use '+' for any type, but mypy doesn't like it, hence the use of str.cat()
        df["AtomicMass"] = (
            df["AtomicNumber"]
            .astype("string")
            .str.cat(df["AtomicMass"].astype("string").str.replace(".", "", regex=False), sep=".")
        )
        df = df.drop(columns=["AtomicNumber"])

        # We need to rescale the error value because we combined the two columns above
        df = df.assign(AtomicMassError=df["AtomicMassError"].astype(float) / 1.0e6)
        df = self.calculate_relative_error(df, "AME")

        df["TableYear"] = self.year
        df["N"] = pd.to_numeric(df["A"]) - pd.to_numeric(df["Z"])
        df["Symbol"] = pd.to_numeric(df["Z"]).map(self.get_symbol)
        df["DataSource"] = 0

        return df.astype(self._data_types())
