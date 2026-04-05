from importlib.resources.abc import Traversable

import pandas as pd

from nuclearmasses.io.nubase_parse import NUBASEParser


class NUBASE:
    """Top level storage and functionality for NUBASE data"""

    def __init__(self, data_path: Traversable):
        self.data_path = data_path
        self.years: list[int] = [1995, 2003, 2012, 2016, 2020]
        self.nubase_files: list[str] = [
            "nubtab97.asc",
            "nubtab03.asc",
            "nubtab12.asc",
            "nubase2016.txt",
            "nubase_1.mas20",
        ]
        self.files: dict[int, str] = dict(zip(self.years, self.nubase_files, strict=True))
        self.nubase_df: pd.DataFrame = self.parse_all_files()

    def get_datafile(self, year: int) -> Traversable:
        """Use the given ``year`` to locate the NUBASE mass table file and return the absolute path."""
        return self.data_path / str(year) / self.files[year]

    def parse_year(self, year: int) -> pd.DataFrame:
        """Parse the file of the given ``year``"""
        return NUBASEParser(filename=self.get_datafile(year), year=year).read_file()

    def parse_all_files(self) -> pd.DataFrame:
        """Parse the files for all available years"""
        return pd.concat((self.parse_year(y) for y in self.years), ignore_index=True)
