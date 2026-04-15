from difflib import get_close_matches
import importlib.resources
import pathlib
import typing

import pandas as pd

from nuclearmasses.io.ame import AME
from nuclearmasses.io.nubase import NUBASE
from nuclearmasses.utils.converter import Converter


class MassTable:
    """Class for all of the mass data.

    Internally there are separate dataframes for the NUBASE and AME data as well as a combined one for all data
    """

    def __init__(self) -> None:
        self._complete_df: pd.DataFrame = self._parse_files()

    def _parse_files(self) -> pd.DataFrame:
        data_path = importlib.resources.files("nuclearmasses").joinpath("data")

        common_columns = ["A", "Z", "N", "TableYear", "Symbol", "DataSource"]

        return pd.merge(AME(data_path).ame_df, NUBASE(data_path).nubase_df, on=common_columns, how="outer")

    def add_user_data(
        self,
        file: str | pathlib.Path | typing.IO,
        source: int = 1,
        common_values: dict[str, typing.Any] | None = None,
    ) -> None:
        """Merge user data into the mass table"""
        # We are going to force at least 3 columns in the user data
        # Two in the input file: A and Z to uniquely identify the isotope
        # One via code: DataSource to differentiate from the original table data
        required_columns = {"A", "Z", "DataSource"}

        # Read the file, should be valid json so nice and simple
        user_df: pd.DataFrame = pd.read_json(file, dtype={"A": int, "Z": int})

        # Add any additional data that is constant for the user data, e.g. TableYear
        if common_values is not None:
            for k, v in common_values.items():
                user_df[k] = v

        # We need to validate the columns so let's get a unique list
        user_columns = set(user_df.columns)
        # The symbol is commonly used so if it wasn't in the file, create it as a column
        if "Symbol" not in user_columns:
            user_df["Symbol"] = pd.to_numeric(user_df["Z"]).map(Converter().get_symbol)

        # Set the source value using the function parameter if it hasn't already been set
        if "DataSource" not in user_columns:
            user_df["DataSource"] = source

        # Refresh user column list
        user_columns = set(user_df.columns)

        # Check we have the necessary columns
        if missing := required_columns - user_columns:
            raise ValueError(f"ERROR: Missing required columns: {missing}")

        # Check any columns, in addition to those required, match the existing ones
        mt_columns = self._complete_df.columns
        if unexpected := user_columns - set(mt_columns):
            for col in unexpected:
                msg = f"ERROR: Column '{col}' not recognised."
                if suggestion := get_close_matches(col, mt_columns, n=1):
                    msg += f" Did you mean '{suggestion[0]}'?"

                raise ValueError(msg)

        # Confirm the provided columns are not empty or null
        if user_df[list(required_columns)].isna().any().any():
            raise ValueError("Required columns have missing values.")

        # Check the user hasn't duplicated rows
        if user_df.duplicated(subset=required_columns).any():
            raise ValueError("Duplicate rows, will not guess which should be used.")

        # Expand the user dataframe to have all the columns present in the mass table, setting those that aren't
        # present to NaN. This isn't strictly necessary as concat aligns automatically, but it should hopefully avoid
        # any issues later on
        user_df = user_df.reindex(columns=mt_columns)

        self._complete_df = pd.concat([self._complete_df, user_df], ignore_index=True)

    @property
    def data(self) -> pd.DataFrame:
        """Access the complete mass table dataframe"""
        return self._complete_df
