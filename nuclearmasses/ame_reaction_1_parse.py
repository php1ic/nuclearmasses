"""Extract the data from the first reaction file."""
import logging
import pathlib

import pandas as pd

from nuclearmasses.ame_reaction_1_file import AMEReactionFileOne


class AMEReactionParserOne(AMEReactionFileOne):
    """Parse the first AME reaction file.

    The format is known but I don't think python can easily parse it.
    """

    def __init__(self, filename: pathlib.Path, year: int):
        """Set the file to read and table year."""
        self.filename = filename
        self.year = year
        super().__init__(self.year)
        logging.info(f"Reading {self.filename} from {self.year}")

    def _column_names(self) -> list[str]:
        """Set the column name depending on the year"""
        match self.year:
            case 2020:
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
        match self.year:
            case 2020:
                return {
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
                        }

    def _na_values(self) -> dict:
        """Set the columns that have placeholder values"""
        match self.year:
            case 2020:
                return {
                        "TwoNeutronSeparationEnergy": ['', '*'],
                        "TwoNeutronSeparationEnergyError": ['', '*'],
                        "TwoProtonSeparationEnergy": ['', '*'],
                        "TwoProtonSeparationEnergyError": ['', '*'],
                        "QAlpha": ['', '*'],
                        "QAlphaError": ['', '*'],
                        "QTwoBeta": ['', '*'],
                        "QTwoBetaError": ['', '*'],
                        "QEpsilon": ['', '*'],
                        "QEpsilonError": ['', '*'],
                        "QBetaNeutron": ['', '*'],
                        "QBetaNeutronError": ['', '*'],
                        }

    def read_file(self) -> pd.DataFrame:
        """Read the file using it's known format

        The AMEReactionFileOne and other functions in this class have hopefully sanitized the
        column names, data types and locations of the date so we can not make the generic
        call to parse the file.
        """
        try:
            df = pd.read_fwf(
                    self.filename,
                    colspecs=self.column_limits,
                    names=self._column_names(),
                    na_values=self._na_values(),
                    keep_default_na=False,
                    on_bad_lines='warn',
                    skiprows=self.HEADER,
                    skipfooter=self.FOOTER
                    )
            df["N"] = df["A"] - df["Z"]
            df["Symbol"] = df["Z"].map(self.z_to_symbol)

            # We use the NUBASE data to define whether or not an isotope is experimentally measured,
            # so for this data we'll just drop any and all '#' characters
            df.replace("#", "", regex=True, inplace=True)

            return df.astype(self._data_types())
        except ValueError as e:
            print(f"Parsing error: {e}")
