import importlib.resources
import typing

import pandas as pd

from nuclearmasses.io.ame import AME
from nuclearmasses.io.nubase import NUBASE


class MassTable:
    """Class for all of the mass data.

    Internally there are separate dataframes for the NUBASE and AME data as well as a combined one for all data
    """

    def __init__(self, df: pd.DataFrame | None = None, filters: list[tuple[str, str, typing.Any]] | None = None):
        self._original_df: pd.DataFrame = self._parse_files() if df is None else df
        self._filters: list[tuple[str, str, typing.Any]] = filters or []
        self._create_dynamic_getters()

    def __repr__(self) -> str:
        """Make printing the class object show the DataFrame nicely"""
        return repr(self.df)

    def __str__(self) -> str:
        """Make printing the class object show the DataFrame nicely"""
        return str(self.df)

    def __getattr__(self, attr: str) -> typing.Any:
        """Delegate pandas methods for deeper chaining"""
        if hasattr(self.df, attr):
            return getattr(self.df, attr)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attr}'")

    def __dir__(self):
        """Pass the pandas api through so we can get autocomplete"""
        return sorted(set(list(self.__dict__.keys()) + dir(type(self)) + dir(self.df)))

    # def __len__(self) -> int:
    #     return len(self.df)
    #
    # def __iter__(self):
    #     return iter(self.df)
    #
    def __getitem__(self, key):
        return type(self)(df=self.df[key])

    def get(self, column: str, value: typing.Any) -> typing.Self:
        """Generic getter: all_data.get('A', 123)"""
        new_filters = self._filters + [(column, "==", value)]
        return type(self)(df=self._original_df, filters=new_filters)

    def filter(self, expr: str) -> typing.Self:
        """Allow arbitrary pandas .query() expressions."""
        # For simplicity we still store as tuples; you could store raw expressions too
        new_filters = self._filters + [("query", expr, None)]
        return type(self)(df=self._original_df, filters=new_filters)

    def _parse_files(self) -> pd.DataFrame:
        data_path = importlib.resources.files("nuclearmasses").joinpath("data")

        common_columns = ["A", "Z", "N", "TableYear", "Symbol"]

        return pd.merge(AME(data_path).ame_df, NUBASE(data_path).nubase_df, on=common_columns, how="outer")

    @property
    def df(self) -> pd.DataFrame:
        """Apply all filters only when .df is accessed"""
        result = self._original_df
        for key, op, val in self._filters:
            if op == "==":
                # Filter on the index
                if key == self._original_df.index.name:
                    result = result[result.index == val]
                # Filter on a regular column
                else:
                    result = result[result[key] == val]
            elif key == "query":
                result = result.query(op)
        return result

    def _create_dynamic_getters(self):
        """Automatically create get_colname(value) methods for every column."""
        for col in self._original_df.columns:
            method_name = f"get_{col}"

            def make_getter(column: str):
                def getter(self, value: typing.Any) -> MassTable:
                    new_filters = self._filters + [(column, "==", value)]
                    return type(self)(df=self._original_df, filters=new_filters)

                return getter

            # Attach the method to the class/instance
            setattr(self, method_name, make_getter(col).__get__(self, MassTable))
