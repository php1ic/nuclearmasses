"""
The ame_reaction_1_file module defines the ``AMEReactionOneLayout`` and ``AMEReactionOneFile`` classes.
The ``AMEreactionOneLayout`` class acts like a base class, storing the common column names and the start and end
positions of the values within the AME data file. The positions change as time progress so the ``AMEReactionOneFile``
class uses the year, passed as a parameter, to update the values as required.

The years 1995, 2003, 2012 and 2016 have identical formatting so are used as the base, not the 1983 format.
"""

import dataclasses


@dataclasses.dataclass(kw_only=True)
class AMEReactionOneLayout:
    """
    Storage class for the most common data in the AME Reaction 1 data file.

    The AME Reaction 1 data file is fixed-width file format so we will store the format details in this class.

    Note we have not listed all parameters in the attributes section as there are so many. The naming convention is
    however shown, along with a description.

    The attribute names align with column names as a string to allow dynamic creation of other variables and attributes
    in other parts of the code.

    Attributes
    ----------
    HEADER : int
        The number of lines in the file to be interpreted as the header.
    FOOTER : int
        The number of lines in the file to be interpreted as the footer.
    START_X : int
        The first column of parameter X.
    END_X : int or None
        The last column of parameter X or None to represent the end of the line.
    column : list[str]
        The list of columns that appear in the file
    positions : list[tuple[str, str, str]]
        A list of tuples detailing column name alongside start and end position in the line.
    """

    HEADER: int = 39
    FOOTER: int = 0
    START_A: int = 1
    END_A: int = 4
    START_Z: int = 8
    END_Z: int = 11
    START_TwoNeutronSeparationEnergy: int = 14
    END_TwoNeutronSeparationEnergy: int = 22
    START_TwoNeutronSeparationEnergyError: int = 23
    END_TwoNeutronSeparationEnergyError: int = 30
    START_TwoProtonSeparationEnergy: int = 32
    END_TwoProtonSeparationEnergy: int = 40
    START_TwoProtonSeparationEnergyError: int = 41
    END_TwoProtonSeparationEnergyError: int = 48
    START_QAlpha: int = 50
    END_QAlpha: int = 58
    START_QAlphaError: int = 59
    END_QAlphaError: int = 66
    START_QTwoBeta: int = 67
    END_QTwoBeta: int = 76
    START_QTwoBetaError: int = 77
    END_QTwoBetaError: int = 84
    START_QEpsilon: int = 85
    END_QEpsilon: int = 94
    START_QEpsilonError: int = 95
    END_QEpsilonError: int = 102
    START_QBetaNeutron: int = 103
    END_QBetaNeutron: int = 112
    START_QBetaNeutronError: int = 113
    END_QBetaNeutronError: int = 125

    def __post_init__(self) -> None:
        self.columns: list[str] = [
            "A",
            "Z",
            "TwoNeutronSeparationEnergy",
            "TwoNeutronSeparationEnergyError",
            "TwoProtonSeparationEnergy",
            "TwoProtonSeparationEnergyError",
            "QAlpha",
            "QAlphaError",
            "QTwoBeta",
            "QTwoBetaError",
            "QEpsilon",
            "QEpsilonError",
            "QBetaNeutron",
            "QBetaNeutronError",
        ]

        self.positions: list[tuple[str, str, str]] = [(f"{c}", f"START_{c}", f"END_{c}") for c in self.columns]


class AMEReactionOneFile:
    """
    Storage class for the year specific data in the AME reaction 1 data file.

    The base `AMEReactionOneLayout`` class is constructed and updated as required for the given ``year``.

    Parameters
    ----------
    year : int
        The year the file being parsed was published

    Attributes
    ----------
    YEAR_OVERRIDES : dict[int | str, dict[str, int]]
        Year specific updates and changes required to ``AMEReactionOneLayout``.
    layout : AMEReactionOneLayout
        A storage class containing details of parameters and their locations in the line.
    """

    YEAR_OVERRIDES: dict[int | str, dict[str, int]] = {
        "default": {},
        1983: {
            "HEADER": 30,
            "START_TwoNeutronSeparationEnergyError": 24,
            "END_TwoNeutronSeparationEnergyError": 30,
            "START_TwoProtonSeparationEnergy": 32,
            "END_TwoProtonSeparationEnergy": 39,
            "START_TwoProtonSeparationEnergyError": 43,
            "END_TwoProtonSeparationEnergyError": 47,
            "START_QAlpha": 50,
            "END_QAlpha": 57,
            "START_QAlphaError": 60,
            "END_QAlphaError": 65,
            "START_QTwoBeta": 68,
            "END_QTwoBeta": 75,
            "START_QTwoBetaError": 78,
            "END_QTwoBetaError": 83,
            "START_QEpsilon": 86,
            "END_QEpsilon": 93,
            "START_QEpsilonError": 96,
            "END_QEpsilonError": 101,
            "START_QBetaNeutron": 103,
            "END_QBetaNeutron": 111,
            "START_QBetaNeutronError": 114,
            "END_QBetaNeutronError": 119,
        },
        1993: {
            "HEADER": 40,
        },
        # 1995 - 2016 are the base years
        1995: {},
        2003: {},
        2012: {},
        2016: {},
        2020: {
            "END_TwoNeutronSeparationEnergy": 24,
            "START_TwoNeutronSeparationEnergyError": 25,
            "END_TwoNeutronSeparationEnergyError": 34,
            "START_TwoProtonSeparationEnergy": 36,
            "END_TwoProtonSeparationEnergy": 46,
            "START_TwoProtonSeparationEnergyError": 47,
            "END_TwoProtonSeparationEnergyError": 56,
            "START_QAlpha": 58,
            "END_QAlpha": 68,
            "START_QAlphaError": 69,
            "END_QAlphaError": 78,
            "START_QTwoBeta": 79,
            "END_QTwoBeta": 90,
            "START_QTwoBetaError": 91,
            "END_QTwoBetaError": 100,
            "START_QEpsilon": 101,
            "END_QEpsilon": 112,
            "START_QEpsilonError": 113,
            "END_QEpsilonError": 122,
            "START_QBetaNeutron": 123,
            "END_QBetaNeutron": 134,
            "START_QBetaNeutronError": 135,
            "END_QBetaNeutronError": 144,
        },
    }

    def __init__(self, year: int) -> None:
        self.layout = AMEReactionOneLayout(
            **AMEReactionOneFile.YEAR_OVERRIDES.get(year, AMEReactionOneFile.YEAR_OVERRIDES["default"])
        )
