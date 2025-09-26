"""Extract the data from the AME mass file."""
import logging
import pathlib

import pandas as pd

from nuclearmasses.ame_mass_file import AMEMassFile


class AMEMassParser(AMEMassFile):
    """Parse the AME mass file.

    The format is known but the provided string does not match all lines.
    We will therefore use START and END markers, which are inherited, and
    read the columns are interested in.
    """

    def __init__(self, filename: pathlib.Path, year: int):
        """Set the file to read and table year"""
        self.filename: pathlib.Path = filename
        self.year: int = year
        super().__init__(self.year)
        logging.info(f"Reading {self.filename} from {self.year}")

    def _column_names(self) -> list[str]:
        """Set the column name depending on the year"""
        match self.year:
            case 2020:
                return [
                        "Z",
                        "A",
                        "MassExcess",
                        "MassExcessError",
                        "BindingEnergyPerA",
                        "BindingEnergyPerAError",
                        "BetaDecayEnergy",
                        "BetaDecayEnergyError",
                        "AtomicMass",
                        "AtomicMassError"
                        ]

    def _data_types(self) -> dict:
        """Set the data type depending on the year"""
        match self.year:
            case 2020:
                return {
                        "Symbol": "string",
                        "N": "Int64",
                        "Z": "Int64",
                        "A": "Int64",
                        "MassExcess": "float64",
                        "MassExcessError": "float64",
                        "BindingEnergyPerA": "float64",
                        "BindingEnergyPerAError": "float64",
                        "BetaDecayEnergy": "float64",
                        "BetaDecayEnergyError": "float64",
                        "AtomicMass": "float64",
                        "AtomicMassError": "float64",
                        }

    def _na_values(self) -> dict:
        """Set the columns that have placeholder values"""
        match self.year:
            case 2020:
                return {
                        "BetaDecayEnergy": ['', '*'],
                        "BetaDecayEnergyError": ['', '*'],
                        }

    def read_file(self) -> pd.DataFrame:
        """Read the file using it's known format

        The AMEMassFile and other functions in this class have hopefully sanitized the
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

            # We skipped the reading of the initial part of the atomic mass as it's always the same as A.
            # Add it back on here and remove the now redundant decimal point from the other part of the number.
            df["AtomicMass"] = df["A"].astype(str) + "." + df["AtomicMass"].str.replace(".", "", regex=False)

            return df.astype(self._data_types())
        except ValueError as e:
            print(f"Parsing error: {e}")

