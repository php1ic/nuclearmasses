"""Extract the date from the second reaction file."""
import logging
import pathlib

import pandas as pd

from nuclearmasses.ame_reaction_2_file import AMEReactionFileTwo


class AMEReactionParserTwo(AMEReactionFileTwo):
    """Parse the second AME reaction file.

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
        """Set the data type depending on the year"""
        match self.year:
            case 2020:
                return {
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
                        }

    def _na_values(self) -> dict:
        """Set the columns that have placeholder values"""
        match self.year:
            case 2020:
                return {
                        "OneNeutronSeparationEnergy": ['', '*'],
                        "OneNeutronSeparationEnergyError": ['', '*'],
                        "OneProtonSeparationEnergy": ['', '*'],
                        "OneProtonSeparationEnergyError": ['', '*'],
                        "QFourBeta": ['', '*'],
                        "QFourBetaError": ['', '*'],
                        "QDeuteronAlpha": ['', '*'],
                        "QDeuteronAlphaError": ['', '*'],
                        "QProtonAlpha": ['', '*'],
                        "QProtonAlphaError": ['', '*'],
                        "QNeutronAlpha": ['', '*'],
                        "QNeutronAlphaError": ['', '*'],
                        }

    def read_file(self) -> pd.DataFrame:
        """Read the file using it's known format

        The AMEReactionFileTwo and other functions in this class have hopefully sanitized the
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
            # The column headers are repeated in this file so need to be removed
            df = df[df['A'] != 'A']
            # Repeated column heading also means we have to cast to create new columns
            df["N"] = pd.to_numeric(df["A"]) - pd.to_numeric(df["Z"])
            df["Symbol"] = pd.to_numeric(df["Z"]).map(self.z_to_symbol)

            # We use the NUBASE data to define whether or not an isotope is experimentally measured,
            # so for this data we'll just drop any and all '#' characters
            df.replace("#", "", regex=True, inplace=True)

            return df.astype(self._data_types())
        except ValueError as e:
            print(f"Parsing error: {e}")
