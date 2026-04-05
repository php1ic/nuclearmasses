import importlib
from importlib.resources.abc import Traversable
import os
import typing

import astropy  # type: ignore[import-untyped]
import numpy as np
import pandas as pd

# Typing hint Union for the different ways a file or data can be represented
DataInput = Traversable | os.PathLike[str] | str | typing.TextIO


class Converter:
    """A utility class for converting between symbol and Z value

    This class provides bidirectional lookup functionality via two dictionaries one mapping Z to symbol,
    and the other symbol to Z.
    """

    def __init__(self, **kwargs) -> None:
        """Construct the symbol -> Z and Z -> symbol dictionaries."""
        # We are using multiple inheritance, so need this for MRO
        super().__init__(**kwargs)
        # fmt: off
        # Formatter wants to put each item on it's own line, I don't
        self.z_to_symbol: dict[int, str] = {
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
            100: "Fm", 101: "Md", 102: "No", 103: "Lr", 104: "Rf", 105: "Db", 106: "Sg", 107: "Bh", 108: "Hs", 109: "Mt", # noqa: E501
            110: "Ds", 111: "Rg", 112: "Cn", 113: "Ed", 114: "Fl", 115: "Ef", 116: "Lv", 117: "Ts", 118: "Og"
        }
        # fmt: on

        # Switch the keys and values of the z_to_symbol dictionary so a user can access the Z value using the symbol
        self.symbol_to_z: dict[str, int] = {val: key for key, val in self.z_to_symbol.items()}

    def get_symbol(self, z: int) -> str | None:
        """Get the symbol representing <z>

        This is a nicely named, very thin wrapper around the inbuilt dictionary.
        I'm sure I was going to do something else in this function beyond basic accessing, but don't recall.
        Leave as is and hopefully I'll remember
        """
        return self.z_to_symbol.get(z, None)

    def get_z(self, symbol: str) -> int | None:
        """Get the z (proton number) representing <symbol>

        This is a nicely named, very thin wrapper around the inbuilt dictionary.
        """
        return self.symbol_to_z.get(symbol, None)

    @staticmethod
    def normalise_symbol(symbol: str) -> str:
        """Validate format of <symbol> to allow simpler conversions

        Element symbols always have a capital first letter and lower case second, if it exists. We store all symbols
        like this so want any user input to be of this format. In typesetting, this is known as title case so we can
        leverage that conversion function.

        No checking is done on the validity of the symbol.
        """
        return symbol.strip().title()

    def unit_to_seconds(self, unit_str: str) -> float:
        """Convert a time unit to a scale factor in seconds.

        Returns np.nan for non-valid time units.

        e.g.
        "s" -> 1.0,
        "min" -> 60.0,
        "keV" -> np.nan
        2 -> np.nan
        """
        if pd.isna(unit_str) or type(unit_str) is not str:
            return np.nan

        # Remove white space and make lower case to be consistent
        cleaned_unit = unit_str.strip().lower()
        if not cleaned_unit:
            return np.nan

        # Use 'silent' so failure is written into the variable, not thrown as an exception
        unit = astropy.units.Unit(cleaned_unit, parse_strict="silent")
        # Check for failures as mentioned above
        if isinstance(unit, astropy.units.UnrecognizedUnit):
            return np.nan

        # We now know the unit is physically valid, but not that it's time related, e.g. minutes rather than km
        # Astropy allows us to check that
        if unit.physical_type != "time":
            return np.nan

        return float(unit.to(astropy.units.s))

    @staticmethod
    def read_fwf(base: DataInput, **kwargs):
        """Overloaded version of pandas.read_fwf() that accepts more types

        Our use of importlib.resource means we have types that the pandas version of read_fwf does not accept.
        It can still be used but some work is required. This function does that work, as well as some other checking
        to make sure we can pass the necessary types into our parser classes.
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
