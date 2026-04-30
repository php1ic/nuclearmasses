"""
The converter module defines the ``Converter`` class that is used to store lookup dictionaries to allow simple and fast
conversions between scientific units and seconds, and element symbol and Z value. The dictionaries are defined on the
class level so any instance should share a single copy.
"""

import importlib
from importlib.resources.abc import Traversable
import os
import typing

import pandas as pd

# Typing hint Union for the different ways a file or data can be represented
DataInput = Traversable | os.PathLike[str] | str | typing.TextIO


class Converter:
    """
    Utility class to convert between various physical properties.

    All methods are static so it is not necessary to create an instance of the class.

    Internal dictionaries allow bidirectional conversion between element symbol and Z, as well as the conversion of an
    time unit in SI format into the equivalent number of seconds (e.g. min -> 60.0).
    """

    UNIT_TO_SECONDS: dict[str, float] = {
        "s": 1.0,
        "ms": 1e-3,
        "us": 1e-6,
        "ns": 1e-9,
        "ps": 1e-12,
        "as": 1e-18,
        "zs": 1e-21,
        "ys": 1e-24,
        "min": 60.0,
        "h": 3600.0,
        "d": 86400.0,
        "yr": 31_557_600.0,  # 365.25 days
        "kyr": 3.15576e10,
        "myr": 3.15576e13,
        "gyr": 3.15576e16,
        "zyr": 3.15576e21,
        "eyr": 3.15576e18,
        "pyr": 3.15576e15,
        "tyr": 3.15576e12,
        "yyr": 3.15576e24,
    }

    # fmt: off
    # Formatter wants to put each item on it's own line, I don't
    Z_TO_SYMBOL: dict[int, str] = {
        0: "n", 1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O", 9: "F",
        10: "Ne", 11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P", 16: "S", 17: "Cl", 18: "Ar", 19: "K",
        20: "Ca", 21: "Sc", 22: "Ti", 23: "V", 24: "Cr", 25: "Mn", 26: "Fe", 27: "Co", 28: "Ni", 29: "Cu",
        30: "Zn", 31: "Ga", 32: "Ge", 33: "As", 34: "Se", 35: "Br", 36: "Kr", 37: "Rb", 38: "Sr", 39: "Y",
        40: "Zr", 41: "Nb", 42: "Mo", 43: "Tc", 44: "Ru", 45: "Rh", 46: "Pd", 47: "Ag", 48: "Cd", 49: "In",
        50: "Sn", 51: "Sb", 52: "Te", 53: "I", 54: "Xe", 55: "Cs", 56: "Ba", 57: "La", 58: "Ce", 59: "Pr",
        60: "Nd", 61: "Pm", 62: "Sm", 63: "Eu", 64: "Gd", 65: "Tb", 66: "Dy", 67: "Ho", 68: "Er", 69: "Tm",
        70: "Yb", 71: "Lu", 72: "Hf", 73: "Ta", 74: "W", 75: "Re", 76: "Os", 77: "Ir", 78: "Pt", 79: "Au",
        80: "Hg", 81: "Tl", 82: "Pb", 83: "Bi", 84: "Po", 85: "At", 86: "Rn", 87: "Fr", 88: "Ra", 89: "Ac",
        90: "Th", 91: "Pa", 92: "U", 93: "Np", 94: "Pu", 95: "Am", 96: "Cm", 97: "Bk", 98: "Cf", 99: "Es",
        100: "Fm", 101: "Md", 102: "No", 103: "Lr", 104: "Rf", 105: "Db", 106: "Sg", 107: "Bh", 108: "Hs", 109: "Mt",
        110: "Ds", 111: "Rg", 112: "Cn", 113: "Ed", 114: "Fl", 115: "Ef", 116: "Lv", 117: "Ts", 118: "Og"
    }
    # fmt: on

    # Switch the keys and values of the z_to_symbol dictionary so a user can access the Z value using the symbol
    SYMBOL_TO_Z: dict[str, int] = {val: key for key, val in Z_TO_SYMBOL.items()}

    def __init__(self, **kwargs) -> None:
        # We are using multiple inheritance, so need this for MRO
        super().__init__(**kwargs)

    @staticmethod
    def get_symbol(z: int) -> str | None:
        """
        Get the symbol representing ``z``.

        This is a nicely named, very thin wrapper around the inbuilt dictionary get.

        Parameters
        ----------
        z : int
            The Z value to get the symbol for.

        Returns
        -------
        str or None
            The string representing the ``z` value or None if the ``z` value is invalid.
        """
        return Converter.Z_TO_SYMBOL.get(z, None)

    @staticmethod
    def get_z(symbol: str) -> int | None:
        """
        Get the z (proton number) representing ``symbol``.

        This is a nicely named, very thin wrapper around the inbuilt dictionary.

        Parameters
        ----------
        symbol : str
            The elemental symbol to get the Z for.

        Returns
        -------
        int or None
            The Z value representing ``symbol`` or None if ``symbol`` is invalid.
        """
        return Converter.SYMBOL_TO_Z.get(symbol, None)

    @staticmethod
    def normalise_symbol(symbol: str) -> str:
        """
        Validate format of ``symbol`` to allow simpler conversions.

        Element symbols always have a capital first letter and lower case second, if it exists. We store all symbols
        like this so want any user input to be of this format. In typesetting, this is known as title case so we can
        leverage that conversion function.

        No checking is done on the validity of the symbol.

        Parameters
        ----------
        symbol : str
            The elemental symbol to validate.

        Returns
        -------
        str
            The elemental symbol with the correct casing.
        """
        return symbol.strip().title()

    @staticmethod
    def unit_to_seconds(unit_str: str) -> float | None:
        """Convert a time unit to a scale factor in seconds.

        Parameters
        ----------
        unit_str : str
            The time unit to convert into seconds.

        Returns
        -------
        float or None
            The time unit represented in seconds or None if the unit does not represent time.

        Examples
        --------
        >>> from nuclearmasses.utils.converter import Converter
        >>> Converter.unit_to_seconds("s")
        1.0
        >>> Converter.unit_to_seconds("min")
        60.0
        >>> Converter.unit_to_seconds("keV")
        >>> Converter.unit_to_seconds(2)
        >>>
        """
        if pd.isna(unit_str) or not isinstance(unit_str, str):
            return None

        # Remove white space and make lower case to be consistent
        cleaned_unit = unit_str.strip().lower()
        if not cleaned_unit:
            return None

        return Converter.UNIT_TO_SECONDS.get(cleaned_unit, None)

    @staticmethod
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

    @staticmethod
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
