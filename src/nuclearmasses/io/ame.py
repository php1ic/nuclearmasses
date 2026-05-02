"""
The ame module defines the ``AME`` class to work on and store details related to the AME data.
"""

from importlib.resources.abc import Traversable

import pandas as pd

from nuclearmasses.io.ame_mass_parse import AMEMassParser
from nuclearmasses.io.ame_reaction_1_parse import AMEReactionParserOne
from nuclearmasses.io.ame_reaction_2_parse import AMEReactionTwoParser


class AME:
    """
    Container class to store details related to the years a AME table was published.

    This is a high level class that tracks details, but delegates the parsing of the files.

    Parameters
    ----------
    data_path : Traversable
        Absolute path to the data files location. Not an actual file, rather the top level directory that contains from
        where we access the year then individual file

    Attributes
    ----------
    data_path : Traversable
        Absolute path to the data files location. Not an actual file, rather the top level directory that contains from
        where we access the year then individual file.
    years : list[ints]
        An ordered list of the years in which a NUBASE table was published.
    ame_files : list[tuple[str, str, str]]
        The filenames each AME data file in year order.
    files : dict[int, tuple[str, str, str]]
        A dictionary mapping published year to filename.
    nubase_df : pandas.DataFrame
        A dataframe containing the NUBASE data from all published years.
    """

    def __init__(self, data_path: Traversable):
        self.data_path = data_path
        self.years: list[int] = [1983, 1993, 1995, 2003, 2012, 2016, 2020]
        self.ame_files: list[tuple[str, str, str]] = [
            ("mass.mas83", "rct1.mas83", "rct2.mas83"),
            ("mass_exp.mas93", "rct1_exp.mas93", "rct2_exp.mas93"),
            ("mass_exp.mas95", "rct1_exp.mas95", "rct2_exp.mas95"),
            ("mass.mas03", "rct1.mas03", "rct2.mas03"),
            ("mass.mas12", "rct1.mas12", "rct2.mas12"),
            ("mass16.txt", "rct1-16.txt", "rct2-16.txt"),
            ("mass.mas20", "rct1.mas20", "rct2.mas20"),
        ]
        self.files: dict[int, tuple[str, str, str]] = dict(zip(self.years, self.ame_files, strict=True))
        self.ame_df: pd.DataFrame = self.parse_all_years()

    def get_datafiles(self, year: int) -> tuple[Traversable, Traversable, Traversable]:
        """
        Construct the absolute paths to the files for the given ``year``.

        Parameters
        ----------
        year : int
            The published year to get the file for.

        Returns
        -------
        tuple[Traversable,Traversable,Traversable]
            The absolute paths to the three AME data files.
        """
        root = self.data_path / str(year)
        mass, rct1, rct2 = self.files[year]

        return root / mass, root / rct1, root / rct2

    def parse_year(self, year: int) -> pd.DataFrame:
        """
        Parse the data from the given ``year``.

        Parameters
        ----------
        year : int
            The published year to get the data for.

        Returns
        -------
        pandas.DataFrame
            The data from ``year`` as a dataframe
        """
        ame_mass, ame_reaction_1, ame_reaction_2 = self.get_datafiles(year)

        mass_df = AMEMassParser(filename=ame_mass, year=year).read_file()
        rct1_df = AMEReactionParserOne(filename=ame_reaction_1, year=year).read_file()
        rct2_df = AMEReactionTwoParser(filename=ame_reaction_2, year=year).read_file()

        # Merge all 3 of the AME dataframes into one
        common_columns = ["A", "Z", "N", "TableYear", "Symbol", "DataSource"]
        return mass_df.merge(rct1_df, on=common_columns, how="outer").merge(rct2_df, on=common_columns, how="outer")

    def parse_all_years(self) -> pd.DataFrame:
        """
        Parse the files for all available years.

        Returns
        -------
        pandas.DataFrame
            The data from all published years as a single dataframe.
        """
        return pd.concat((self.parse_year(y) for y in self.years), ignore_index=True)
