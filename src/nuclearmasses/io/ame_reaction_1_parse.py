"""
The ame_reaction_1_parse module defines the ``AMEReactionOneParser`` class. This class contains the logic required to
sort and organise the inputs to :meth:`pandas.read_fwf` dependent on the year of the file. Once parsed, known typos and
inconsistencies are cleaned from the resultant dataframe.
"""

import pandas as pd

from nuclearmasses.io.ame_reaction_1_file import AMEReactionOneFile
from nuclearmasses.utils.converter import Converter, DataInput


class AMEReactionOneParser:
    """
    Parse the first AME reaction file, doing the necessary preparation and clean ups of data.

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
        self.filename: DataInput = filename
        self.year = year
        self.layout = AMEReactionOneFile(year).layout

        self.column_limits = [
            (getattr(self.layout, start), getattr(self.layout, end)) for _, start, end in self.layout.positions
        ]

    def _column_names(self) -> list[str]:
        """
        Set the column name depending on the year.

        Returns
        -------
        list[str]
            An ordered list of the columns that exist in the file.
        """
        return self.layout.columns

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
            "A": "Int64",
            "Z": "Int64",
            "N": "Int64",
            "TwoNeutronSeparationEnergy": "float64",
            "TwoNeutronSeparationEnergyError": "float64",
            "TwoProtonSeparationEnergy": "float64",
            "TwoProtonSeparationEnergyError": "float64",
            "QAlpha": "float64",
            "QAlphaError": "float64",
            "QTwoBeta": "float64",
            "QTwoBetaError": "float64",
            "QEpsilon": "float64",
            "QEpsilonError": "float64",
            "QBetaNeutron": "float64",
            "QBetaNeutronError": "float64",
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
        return {
            "A": [""],
            "TwoNeutronSeparationEnergy": ["", "*"],
            "TwoNeutronSeparationEnergyError": ["", "*"],
            "TwoProtonSeparationEnergy": ["", "*"],
            "TwoProtonSeparationEnergyError": ["", "*"],
            "QAlpha": ["", "*"],
            "QAlphaError": ["", "*"],
            "QTwoBeta": ["", "*"],
            "QTwoBetaError": ["", "*"],
            "QEpsilon": ["", "*"],
            "QEpsilonError": ["", "*"],
            "QBetaNeutron": ["", "*"],
            "QBetaNeutronError": ["", "*"],
        }

    def read_file(self) -> pd.DataFrame:
        """
        Read the file-like object ``self.filename`` into a dataframe

        The ``AMEReactionOneFile`` and other functions in this class have hopefully sanitized the column names, data
        types and locations of the date so we can now make the generic call to parse the file.

        Returns
        -------
        pandas.DataFrame
            A dataframe containing the parsed and organised contents of the first AME reaction data file
        """
        df = Converter.read_fwf(
            self.filename,
            colspecs=self.column_limits,
            names=self._column_names(),
            na_values=self._na_values(),
            keep_default_na=False,
            on_bad_lines="warn",
            skiprows=self.layout.HEADER,
            skipfooter=self.layout.FOOTER,
        )
        # We use the NUBASE data to define whether or not an isotope is experimentally measured,
        # so for this data we'll just drop any and all '#' characters
        df = Converter.strip_char_from_string_columns(df, "#")

        if self.year == 1983:
            # The column headers and units are repeated in the 1983 table
            df = df[(df["A"] != "A") & (df["Z"] != "")]
            # The A value is not in the column if it doesn't change so we need to fill down
            df["A"] = df["A"].ffill()

        df["TableYear"] = self.year
        df["N"] = pd.to_numeric(df["A"]) - pd.to_numeric(df["Z"])
        df["Symbol"] = pd.to_numeric(df["Z"]).map(Converter.get_symbol)
        df["DataSource"] = 0

        return df.astype(self._data_types())
