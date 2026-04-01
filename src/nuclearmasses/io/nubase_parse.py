import logging
import typing

import pandas as pd

from nuclearmasses.io.nubase_file import NUBASEFile
from nuclearmasses.utils.converter import Converter, DataInput


class NUBASEParser(NUBASEFile, Converter):
    """Parse the NUBASE data file.

    A collection of functions to parse the weird format of the NUBASE file.
    """

    def __init__(self, filename: DataInput, year: int):
        """Set the file to read and the table year."""
        super().__init__(year=year)
        self.filename: DataInput = filename
        self.year: int = year
        self.unit_replacements: dict[str, str] = {
            r"y$": "yr",
            r"^m$": "min",
        }
        logging.info(f"Reading {self.filename} from {self.year}")

    def _column_names(self) -> list[str]:
        """Set the column name depending on the year"""
        col_names = [
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

        # The discovery year was added after 2003, and I assume it will be there in the future, so we will set up
        # as if it is always present and delete for the first two tables.
        if self.year == 1995 or self.year == 2003:
            col_names.remove("DiscoveryYear")

        return col_names

    def _data_types(self) -> dict:
        """Set the data type depending on the year"""
        data_types = {
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

        # The discovery year was added after 2003, and I assume it will be there in the future, so we will set up
        # as if it is always present and delete for the first two tables.
        if self.year == 1995 or self.year == 2003:
            data_types.pop("DiscoveryYear")

        return data_types

    def _na_values(self) -> dict:
        """Set the columns that have placeholder values"""
        match self.year:
            case 1995:
                return {
                    "State": [""],
                    "NUBASEMassExcess": [""],
                    "NUBASEMassExcessError": [""],
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
        raw_df["HalfLifeValue"] = raw_df["HalfLifeValue"].astype("object")
        raw_df["HalfLifeError"] = raw_df["HalfLifeError"].astype("object")

        mask = raw_df["HalfLifeValue"] == "stbl"
        raw_df.loc[mask, ["HalfLifeValue", "HalfLifeUnit", "HalfLifeError"]] = (99.99, "Zyr", 0.0)

        raw_df["HalfLifeValue"] = raw_df["HalfLifeValue"].astype("string").str.replace(r"[<>?~]", "", regex=True)
        # We'll be lazy here and remove any characters in this column. Future us will parse this properly
        raw_df["HalfLifeError"] = raw_df["HalfLifeError"].astype("string").str.replace(r"[<>?~a-z]", "", regex=True)

        # Use the 3 half-life columns to create 2 new columns with units of seconds
        raw_df["HalfLifeUnit"] = raw_df["HalfLifeUnit"].astype("string")
        # Bookkeeping: Tidy up know unusual units, i.e. y for years and m for minutes
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

    def parse_state(self, raw_df) -> pd.DataFrame:
        """Interpret the state of the isotope

        Currently we are only interested in ground states, but in the future we will care about isomers.
        """
        # Ignore anything this is not the ground state
        raw_df = raw_df[raw_df["State"] == 0]
        # As 'State' is now necessarily 0 and the Isomer columns are empty, drop them.
        raw_df = raw_df.drop(columns=["State", "IsomerEnergy", "IsomerEnergyError"])

        return raw_df

    def calculate_relative_error(self, raw_df) -> pd.DataFrame:
        """Calculate the relative error of the mass excess

        12C has a 0.0 +/- 0.0 mass excess definition by definition so ensure that is still true.
        """
        raw_df["NUBASERelativeError"] = abs(
            raw_df["NUBASEMassExcessError"].astype(float) / raw_df["NUBASEMassExcess"].astype(float)
        )
        raw_df.loc[(raw_df.Z == 6) & (raw_df.A == 12), "NUBASERelativeError"] = 0.0

        return raw_df

    def read_file(self) -> pd.DataFrame:
        """Read the file using it's known format

        The NUBASEFile and other functions in this class have hopefully sanitized the
        column names, data types and locations of the date so we can now make the generic
        call to parse the file.
        """
        df = Converter.read_fwf(
            self.filename,
            colspecs=typing.cast(typing.Sequence[tuple[int, int]], self.column_limits),  # appease mypy
            names=self._column_names(),
            na_values=self._na_values(),
            keep_default_na=False,
            on_bad_lines="warn",
            skiprows=self.HEADER,
            skipfooter=self.FOOTER,
        )

        df = self.parse_state(df)

        # We use the NUBASE data to define whether or not an isotope is experimentally measured,
        df["Experimental"] = ~df["NUBASEMassExcess"].astype("string").str.contains("#", na=False)
        # Once we have used the '#' to determine if it's experimental or not, we can remove all instances of it
        df.replace("#", "", regex=True, inplace=True)

        df = self.parse_half_life(df)
        df = self.calculate_relative_error(df)

        if self.year == 2012:
            # 198Au has a typo in it's decay mode in the 2012 table. It is recorded as '-'
            df.loc[(df.A == 198) & (df.Z == 79), "DecayModes"] = "B-"

        df["TableYear"] = self.year
        df["N"] = pd.to_numeric(df["A"]) - pd.to_numeric(df["Z"])
        df["Symbol"] = pd.to_numeric(df["Z"]).map(self.get_symbol)

        return df.astype(self._data_types())
