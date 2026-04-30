"""
The nubase module defines the ``NUBASE`` class to work on and store details related to the NUBASE data.
"""

from importlib.resources.abc import Traversable

import pandas as pd

from nuclearmasses.io.nubase_parse import NUBASEParser


class NUBASE:
    """
    Container class to store details related to the years a NUBASE table was published.

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
    nubase_files : list[str]
        The filenames of the NUBASE data files in year order.
    files : dict[int, str]
        A dictionary mapping published year to filename.
    nubase_df : pandas.DataFrame
        A dataframe containing the NUBASE data from all published years.
    """

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
        """
        Construct the absolute path to the mass table file for the given ``year``.

        Parameters
        ----------
        year : int
            The published year to get the file for.

        Returns
        -------
        Traversable
            The absolute path to the data file.
        """
        return self.data_path / str(year) / self.files[year]

    def parse_year(self, year: int) -> pd.DataFrame:
        """
        Parse the data of the given ``year``.

        Parameters
        ----------
        year : int
            The published year to get the data for.

        Returns
        -------
        pandas.DataFrame
            The data from ``year`` as a dataframe
        """
        return NUBASEParser(filename=self.get_datafile(year), year=year).read_file()

    def parse_all_files(self) -> pd.DataFrame:
        """
        Parse the files for all available years.

        Returns
        -------
        pandas.DataFrame
            The data from all published years as a single dataframe.
        """
        return pd.concat((self.parse_year(y) for y in self.years), ignore_index=True)
