import logging
import pathlib
import typing

import pandas as pd

from nuclearmasses.io.nubase_file import NUBASEFile


class NUBASEParser(NUBASEFile):
    """Parse the NUBASE data file.

    A collection of functions to parse the weird format of the NUBASE file.
    """

    def __init__(self, filename: pathlib.Path, year: int):
        """Set the file to read and the table year."""
        super().__init__(year)
        self.filename: pathlib.Path = filename
        self.year: int = year
        self.unit_replacements: dict[str, str] = {
            r"y$": "yr",
            r"^m$": "min",
        }
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
                    "HalfLifeSeconds": "float64",
                    "HalfLifeErrorSeconds": "float64",
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
                    "HalfLifeSeconds": "float64",
                    "HalfLifeErrorSeconds": "float64",
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

    def parse_half_life(self, raw_df) -> pd.DataFrame:
        """Create half-life columns with SI units

        The half-life is stored as a human readable value, e.g. 2ms, 4Gyr, 5mins, this is fine to read but not to do
        any type of sorting or algorithm. Convert to the SI unit of seconds, but don't overwrite original columns.
        """
        # Convert stable isotopes into ones with enormous lifetimes with zero error so we can cast
        # pandas v3 became much stricter with type conversions so convert to object (from string) so
        # we can assign a float without breaking other parts of the code
        raw_df["HalfLifeValue"] = raw_df["HalfLifeValue"].astype("object")
        raw_df["HalfLifeError"] = raw_df["HalfLifeError"].astype("object")

        mask = raw_df["HalfLifeValue"] == "stbl"
        raw_df.loc[mask, ["HalfLifeValue", "HalfLifeUnit", "HalfLifeError"]] = (99.99, "Zyr", 0.0)

        raw_df["HalfLifeValue"] = raw_df["HalfLifeValue"].astype("string").str.replace(r"[<>?~]", "", regex=True)
        # We'll be lazy here and remove any characters in this column. Future us will parse this properly
        raw_df["HalfLifeError"] = raw_df["HalfLifeError"].astype("string").str.replace(r"[<>?~a-z]", "", regex=True)

        # Use the 3 half-life columns to create 2 new columns with units of seconds
        raw_df["HalfLifeUnit"] = raw_df["HalfLifeUnit"].astype("string")
        for pattern, replacement in self.unit_replacements.items():
            raw_df["HalfLifeUnit"] = raw_df["HalfLifeUnit"].str.replace(pattern, replacement, regex=True)

        # Ensure numeric values
        for col in ["HalfLifeValue", "HalfLifeError"]:
            raw_df[col] = pd.to_numeric(raw_df[col], errors="coerce")
        # Pre-compute unit -> second conversions
        unit_map = raw_df["HalfLifeUnit"].map(self.unit_to_seconds)

        raw_df["HalfLifeSeconds"] = raw_df["HalfLifeValue"] * unit_map
        raw_df["HalfLifeErrorSeconds"] = raw_df["HalfLifeError"] * unit_map

        return raw_df

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

            df = self.parse_half_life(df)
        except ValueError as e:
            print(f"Parsing error: {e}")

        return df.astype(self._data_types())
