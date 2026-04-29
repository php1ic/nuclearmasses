"""
The mass_table module defines the ``MassTable`` class that is used to store all the data published by the AME and
NUBASE papers. Once an instance of the class is instantiated, the ``data`` attribute can be used to access the
complete mass table as a pandas Dataframe.
"""

from difflib import get_close_matches
import importlib.resources
import io
import pathlib
import typing

import pandas as pd

from nuclearmasses.io.ame import AME
from nuclearmasses.io.nubase import NUBASE
from nuclearmasses.utils.converter import Converter


class MassTable:
    """
    Container class for the complete mass table

    Any ``MassTable`` instance parses all data files on construction, and has its own copy of the mass table dataframe.
    The dataframe is accessed via the ``data`` attribute, but functionality that manipulates the mass table is generally
    done on the class instance level.

    Attributes
    ----------
    data : pandas.DataFrame
        The parsed mass table and any additional user data.
    """

    def __init__(self) -> None:
        self._complete_df: pd.DataFrame = self._parse_files()

    def _parse_files(self) -> pd.DataFrame:
        """
        Parse all the published data files and merge into a single dataframe

        The merge is carried out on values unique to an isotope, and the published year, to remove duplicated columns.
        No indexing or slicing is done, so the dataframe is in a relatively raw form.

        Returns
        -------
        pandas.DataFrame
            The complete mass table as a pandas dataframe
        """
        data_path = importlib.resources.files("nuclearmasses").joinpath("data")

        common_columns = ["A", "Z", "N", "TableYear", "Symbol", "DataSource"]

        return pd.merge(AME(data_path).ame_df, NUBASE(data_path).nubase_df, on=common_columns, how="outer")

    def add_user_data(
        self,
        data: str | pathlib.Path | typing.IO,
        source: int = 1,
        common_values: dict[str, typing.Any] | None = None,
    ) -> None:
        """
        Add user data into the published mass table

        Read json formatted ``data`` for isotope identification and values then add it to the existing mass table using
        ``source`` to differentiate it from published values. If not present in ``data``, the dictionary
        ``common_values`` can be used to set a single value for a property on all isotopes added.

        The ``data`` is added via :meth:`pandas.concat` to create new entries for each isotope, rather than overwriting.
        It is not merged in via :meth:`pandas.merge` so any values not provided are set to NaN.

        Parameters
        ----------
        data : str | pathlib.Path | typing.IO
            The data, in json format, that will be added to the existing dataframe.
        source : int, default 1
            The value used to identify where this data has originated.
        common_values : dict[str, typing.Any] | None
            Additional values, not provided in ``data`` but common to all entires
        """
        # We are going to force at least 3 columns in the user data
        # Two in the input file: A and Z to uniquely identify the isotope
        # One via code: DataSource to differentiate from the original table data
        required_columns = {"A", "Z", "DataSource"}

        # Is the string a json string or filename
        if isinstance(data, str):
            path = pathlib.Path(data)

            if path.is_file():
                data = path
            else:
                data = io.StringIO(data)

        # Read the data, should be valid json so nice and simple
        user_df: pd.DataFrame = pd.read_json(data, dtype={"A": int, "Z": int})

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
        """
        Return the dataframe containing the complete mass table

        Data from all available years and both AME and NUBASE sources is combined and collated into a single dataframe.

        Returns
        -------
        pandas.DataFrame
            The complete mass table as a pandas dataframe
        """
        return self._complete_df
