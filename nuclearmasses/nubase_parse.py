"""Extract the data from the nubase file."""

import logging
import pathlib
import typing

import pandas as pd

from nuclearmasses.nubase_file import NUBASEFile


class NUBASEParser(NUBASEFile):
    """Parse the NUBASE data file.

    A collection of functions to parse the weird format of the NUBASE file.
    """

    def __init__(self, filename: pathlib.Path, year: int):
        """Set the file to read and the table year."""
        self.filename = filename
        self.year = year
        super().__init__(self.year)
        logging.info(f"Reading {self.filename} from {self.year}")

    def _column_names(self) -> list[str]:
        """Set the column name depending on the year"""
        match self.year:
            case 1995 | 2003:
                return [
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
                    "DecayModes",
                ]
            case _:
                return [
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

    def _data_types(self) -> dict:
        """Set the data type depending on the year"""
        match self.year:
            case 1995 | 2003:
                return {
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
                    "Spin": "string",
                    "DecayModes": "string",
                }
            case _:
                return {
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
                    "Spin": "string",
                    "DiscoveryYear": "Int64",
                    "DecayModes": "string",
                }

    def _na_values(self) -> dict:
        """Set the columns that have placeholder values"""
        match self.year:
            case 1995:
                return {
                    "NUBASEMassExcess": [""],
                    "NUBASEMassExcessError": [""],
                    "State": [""],
                    "HalfLifeValue": [""],
                    "HalfLifeUnit": [""],
                    "HalfLifeError": [""],
                    "Spin": [""],
                    "DecayModes": [""],
                }
            case _:
                return {
                    "State": [""],
                    "NUBASEMassExcess": [""],
                    "NUBASEMassExcessError": [""],
                    "HalfLifeValue": ["", "p-unst", "p-unst#"],
                    "HalfLifeUnit": [""],
                    "HalfLifeError": [""],
                    "DiscoveryYear": [""],
                    "DecayModes": [""],
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
                colspecs=typing.cast(typing.Sequence[tuple[int, int]], self.column_limits),  # appease mypy
                names=self._column_names(),
                na_values=self._na_values(),
                keep_default_na=False,
                on_bad_lines="warn",
                skiprows=self.HEADER,
                skipfooter=self.FOOTER,
            )
            # We use the NUBASE data to define whether or not an isotope is experimentally measured,
            df["Experimental"] = ~df["NUBASEMassExcess"].astype("string").str.contains("#", na=False)
            # Once we have used the '#' to determine if it's experimental or not, we can remove all instances of it
            df.replace("#", "", regex=True, inplace=True)

            df["TableYear"] = self.year
            df["N"] = pd.to_numeric(df["A"]) - pd.to_numeric(df["Z"])
            df["Symbol"] = pd.to_numeric(df["Z"]).map(self.z_to_symbol)
            # For the moment, we will ignore anything this is not the ground state
            df = df[df["State"] == 0]
            # As 'State' is now necessarily 0 and the Isomer columns are empty, drop them.
            df = df.drop(columns=["State", "IsomerEnergy", "IsomerEnergyError"])

            # Convert stable isotopes into ones with enormous lifetimes with zero error so we can cast
            mask = df["HalfLifeValue"] == "stbl"
            df.loc[mask, ["HalfLifeValue", "HalfLifeUnit", "HalfLifeError"]] = (99.99, "Zy", 0.0)

            df["HalfLifeValue"] = df["HalfLifeValue"].astype("string").str.replace(r"[<>?~]", "", regex=True)
            # We'll be lazy here and remove any characters in this column. Future us will parse this properly
            df["HalfLifeError"] = df["HalfLifeError"].astype("string").str.replace(r"[<>?~a-z]", "", regex=True)
        except ValueError as e:
            print(f"Parsing error: {e}")

        return df.astype(self._data_types())
