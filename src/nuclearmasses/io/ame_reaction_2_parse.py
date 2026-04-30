"""
The ame_reaction_2_parse module defines the ``AMEReactionParserTwo`` class. This class contains the logic required to
sort and organise the inputs to :meth:`pandas.read_fwf` dependent on the year of the file. Once parsed, known typos and
inconsistencies are cleaned from the resultant dataframe.
"""

import pandas as pd

from nuclearmasses.io.ame_reaction_2_file import AMEReactionFileTwo
from nuclearmasses.utils.converter import Converter, DataInput


class AMEReactionParserTwo(AMEReactionFileTwo, Converter):
    """
    Parse the second AME reaction file, doing the necessary preparation and clean ups of data.

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
        self.year = year

    def _column_names(self) -> list[str]:
        """
        Set the column name depending on the year.

        Returns
        -------
        list[str]
            An ordered list of the columns that exist in the file.
        """
        return [
            "A",
            "Z",
            "OneNeutronSeparationEnergy",
            "OneNeutronSeparationEnergyError",
            "OneProtonSeparationEnergy",
            "OneProtonSeparationEnergyError",
            "QFourBeta",
            "QFourBetaError",
            "QDeuteronAlpha",
            "QDeuteronAlphaError",
            "QProtonAlpha",
            "QProtonAlphaError",
            "QNeutronAlpha",
            "QNeutronAlphaError",
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
            "A": "Int64",
            "Z": "Int64",
            "N": "Int64",
            "OneNeutronSeparationEnergy": "float64",
            "OneNeutronSeparationEnergyError": "float64",
            "OneProtonSeparationEnergy": "float64",
            "OneProtonSeparationEnergyError": "float64",
            "QFourBeta": "float64",
            "QFourBetaError": "float64",
            "QDeuteronAlpha": "float64",
            "QDeuteronAlphaError": "float64",
            "QProtonAlpha": "float64",
            "QProtonAlphaError": "float64",
            "QNeutronAlpha": "float64",
            "QNeutronAlphaError": "float64",
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
            "OneNeutronSeparationEnergy": ["", "*"],
            "OneNeutronSeparationEnergyError": ["", "*"],
            "OneProtonSeparationEnergy": ["", "*"],
            "OneProtonSeparationEnergyError": ["", "*"],
            "QFourBeta": ["", "*"],
            "QFourBetaError": ["", "*"],
            "QDeuteronAlpha": ["", "*"],
            "QDeuteronAlphaError": ["", "*"],
            "QProtonAlpha": ["", "*"],
            "QProtonAlphaError": ["", "*"],
            "QNeutronAlpha": ["", "*"],
            "QNeutronAlphaError": ["", "*"],
        }

    def read_file(self) -> pd.DataFrame:
        """
        Read the file-like object ``self.filename`` into a dataframe

        The ``AMEReactionTwoFile`` and other functions in this class have hopefully sanitized the column names, data
        types and locations of the date so we can now make the generic call to parse the file.

        Returns
        -------
        pandas.DataFrame
            A dataframe containing the parsed and organised contents of the second AME reaction data file
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
            df = df[(df["A"] != "A") & (df["Z"] != "")]
            # The A value is not in the column if it doesn't change so we need to fill down
            df["A"] = df["A"].ffill()
        elif self.year == 2020:
            # The column headers and units are repeated in the 2020 table
            df = df[(df["A"] != "A") & (df["Z"] != "Z")]

        # Repeated column heading also means we have to cast to create new columns
        df["TableYear"] = self.year
        df["N"] = pd.to_numeric(df["A"]) - pd.to_numeric(df["Z"])
        df["Symbol"] = pd.to_numeric(df["Z"]).map(self.get_symbol)
        df["DataSource"] = 0

        return df.astype(self._data_types())
