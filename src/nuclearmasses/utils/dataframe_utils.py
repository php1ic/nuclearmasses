"""
The module dataframe_utils contains functionality to extend that available via pandas or apply a common transformation
to a dataframe that is used throughout the repository.
"""

import importlib
from importlib.resources.abc import Traversable

import pandas as pd

from nuclearmasses.utils.type_defs import DataInput


def read_fwf(base: DataInput, **kwargs):
    """
    Overloaded version of :meth:`pandas.read_fwf` that accepts additional types.

    The use of importlib.resource means we have types that the pandas version of read_fwf does not accept.
    It can still be used but some work is required. This function does that work, as well as some other checking
    to make sure we can pass the necessary types into our parser classes.

    Parameters
    ----------
    base : DataInput
        The file-like object to read.

    Returns
    -------
    pandas.DataFrame
        The file-like object parsed into a pandas dataframe.
    """
    # A file like object
    if hasattr(base, "read"):
        return pd.read_fwf(base, **kwargs)  # type: ignore[arg-type]

    # importlib.resource Traversable
    if isinstance(base, Traversable):
        with importlib.resources.as_file(base) as the_file:
            return pd.read_fwf(the_file, **kwargs)

    # Filesystem path
    return pd.read_fwf(base, **kwargs)


def strip_char_from_string_columns(df: pd.DataFrame, char: str) -> pd.DataFrame:
    """
    Remove ``char`` from columns that are of known string type

    Helper method to optimise the removal of the ``char`` character from columns in ``df`` that are of string type.
    This function is specific to this module; we know, after parsing a file with :meth:'pandas.read_fwf`, columns
    that contain purely floats will be of type float, but if a value on one line is e.g. 1234.56# the column will
    be of type string (or object). As we wish to remove the '#' character, we can use this detail to only apply the
    removal algorithm to those columns of type string and save some unnecessary processing.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe we are removing the character from.
    char : str
        The character we want to remove.

    Returns
    -------
    pandas.DataFrame
        The original dataframe with all instance of ``char`` removed from string type columns.
    """
    cols = df.select_dtypes(include=["object", "string"]).columns
    df[cols] = df[cols].apply(lambda s: s.str.replace(char, "", regex=False))
    return df


def calculate_relative_error(raw_df: pd.DataFrame, source: str) -> pd.DataFrame:
    """
    Calculate the relative error of the mass excess.

    12C has a 0.0 +/- 0.0 mass excess by definition, so relative error is 0.0. The division by zero will put a NaN
    value in the column for 12C so we will manually correct and set to 0.0.

    Parameters
    ----------
    raw_df : pandas.DataFrame
        The raw dataframe upon which we will act.
    source : str
        Which table's data are we working with

    Returns
    -------
    pandas.DataFrame
        The updated dataframe with a new relative mass excess column.
    """
    raw_df[f"{source}RelativeError"] = abs(
        raw_df[f"{source}MassExcessError"].astype(float) / raw_df[f"{source}MassExcess"].astype(float)
    )
    raw_df.loc[(raw_df.Z == 6) & (raw_df.A == 12), f"{source}RelativeError"] = 0.0

    return raw_df
