import pathlib

import pandas as pd

from nuclearmasses.io.nubase_parse import NUBASEParser


class NUBASE:
    """Top level storage and functionality for NUBASE data"""

    def __init__(self, data_path: pathlib.Path):
        super().__init__()
        self.data_path = data_path
        self.years = [1995, 2003, 2012, 2016, 2020]
        self.nubase_df = pd.concat([self.parse_year(y) for y in self.years], ignore_index=True)

    def get_datafile(self, year: int) -> pathlib.Path:
        """Use the given year to locate the NUBASE mass table file and return the absolute path."""
        nubase_mass = self.data_path / pathlib.Path(str(year))
        nubase_mass = nubase_mass.resolve()

        match year:
            case 1995:
                nubase_mass = nubase_mass / "nubtab97.asc"
            case 2003:
                nubase_mass = nubase_mass / "nubtab03.asc"
            case 2012:
                nubase_mass = nubase_mass / "nubtab12.asc"
            case 2016:
                nubase_mass = nubase_mass / "nubase2016.txt"
            case 2020:
                nubase_mass = nubase_mass / "nubase_1.mas20"

        return nubase_mass

    def parse_year(self, year: int) -> pd.DataFrame:
        """Parse the file of the given ``year``"""
        return NUBASEParser(filename=self.get_datafile(year), year=year).read_file()
