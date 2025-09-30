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
            case _:
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
                        "AtomicMassError"
                        ]

    def _data_types(self) -> dict:
        """Set the data type depending on the year"""
        match self.year:
            case _:
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
                        }

    def _na_values(self) -> dict:
        """Set the columns that have placeholder values"""
        match self.year:
            case 1983:
                return {
                        "A": [''],
                        "BetaDecayEnergy": ['', '*'],
                        "BetaDecayEnergyError": ['', '*'],
                        }
            case _:
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
            # We use the NUBASE data to define whether or not an isotope is experimentally measured,
            # so for this data we'll just drop any and all '#' characters
            df.replace("#", "", regex=True, inplace=True)

            if self.year == 1983:
                # The column headers and units are repeated in the 1983 table
                df = df[(df['A'] != 'A') & (~df["AMEMassExcess"].astype("string").str.contains('keV', na=False))]
                # The A value is not in the column if it doesn't change so we need to fill down
                df['A'] = df['A'].ffill()
                # Isomeric states are sometimes included in this version of the file
                # For each row in the dataframe, if the previous row has equal A and Z, drop the current row
                df = df[~((df['A'] == df['A'].shift()) & (df['Z'] == df['Z'].shift()))]
                # Total binding energy is recorded in this years file so convert to per A to match the other years

            if self.year == 1983 or self.year == 1993 or self.year == 1995:
                df["BindingEnergyPerA"] = df["BindingEnergyPerA"].astype(float) / df['A'].astype(float)
                df["BindingEnergyPerAError"] = df["BindingEnergyPerAError"].astype(float) / df['A'].astype(float)

            df["TableYear"] = self.year
            df["N"] = pd.to_numeric(df["A"]) - pd.to_numeric(df["Z"])
            df["Symbol"] = pd.to_numeric(df["Z"]).map(self.z_to_symbol)

            # Combine the two columns to create the atomic mass then drop the redundant column
            df["AtomicMass"] = df["AtomicNumber"].astype("string") + "." + df["AtomicMass"].astype("string").str.replace(".", "", regex=False)
            df = df.drop(columns=["AtomicNumber"])

            # We need to rescale the error value because we combined the two columns above
            df = df.assign(AtomicMassError=df["AtomicMassError"].astype(float) / 1.0e6)

            return df.astype(self._data_types())
        except ValueError as e:
            print(f"Parsing error: {e}")
