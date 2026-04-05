import importlib.resources

import pandas as pd

from nuclearmasses.io.ame import AME
from nuclearmasses.io.nubase import NUBASE


class MassTable:
    """Class for all of the mass data.

    Internally there are separate dataframes for the NUBASE and AME data as well as a combined one for all data
    """

    def __init__(self) -> None:
        self._complete_df: pd.DataFrame = self._parse_files()

    def _parse_files(self) -> pd.DataFrame:
        data_path = importlib.resources.files("nuclearmasses").joinpath("data")

        common_columns = ["A", "Z", "N", "TableYear", "Symbol"]

        return pd.merge(AME(data_path).ame_df, NUBASE(data_path).nubase_df, on=common_columns, how="outer")

    @property
    def data(self) -> pd.DataFrame:
        """Access the complete mass table dataframe"""
        return self._complete_df
