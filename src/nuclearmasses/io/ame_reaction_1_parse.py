import logging

import pandas as pd

from nuclearmasses.io.ame_reaction_1_file import AMEReactionFileOne
from nuclearmasses.utils.converter import Converter, DataInput


class AMEReactionParserOne(AMEReactionFileOne, Converter):
    """Parse the first AME reaction file.

    The format is known but I don't think python can easily parse it.
    """

    def __init__(self, filename: DataInput, year: int):
        """Set the file to read and table year."""
        super().__init__(year=year)
        self.filename: DataInput = filename
        self.year = year
        logging.info(f"Reading {self.filename} from {self.year}")

    def _column_names(self) -> list[str]:
        """Set the column name depending on the year"""
        return [
            "A",
            "Z",
            "TwoNeutronSeparationEnergy",
            "TwoNeutronSeparationEnergyError",
            "TwoProtonSeparationEnergy",
            "TwoProtonSeparationEnergyError",
            "QAlpha",
            "QAlphaError",
            "QTwoBeta",
            "QTwoBetaError",
            "QEpsilon",
            "QEpsilonError",
            "QBetaNeutron",
            "QBetaNeutronError",
        ]

    def _data_types(self) -> dict:
        """Set the data type depending on the year"""
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
        """Set the columns that have placeholder values"""
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
        """Read the file using it's known format

        The AMEReactionFileOne and other functions in this class have hopefully sanitized the
        column names, data types and locations of the date so we can now make the generic
        call to parse the file.
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
        df = df.replace("#", "", regex=True)

        if self.year == 1983:
            # The column headers and units are repeated in the 1983 table
            df = df[(df["A"] != "A") & (df["Z"] != "")]
            # The A value is not in the column if it doesn't change so we need to fill down
            df["A"] = df["A"].ffill()

        df["TableYear"] = self.year
        df["N"] = pd.to_numeric(df["A"]) - pd.to_numeric(df["Z"])
        df["Symbol"] = pd.to_numeric(df["Z"]).map(self.get_symbol)
        df["DataSource"] = 0

        return df.astype(self._data_types())
