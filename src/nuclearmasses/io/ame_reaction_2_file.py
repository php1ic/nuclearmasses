"""
The ame_reaction_2_file module defines the ``AMEReactionTwoLayout`` and ``AMEReactionTwoFile`` classes.
The ``AMEreactionTwoLayout`` class acts like a base class, storing the common column names and the start and end
positions of the values within the AME data file. The positions change as time progress so the ``AMEReactionTwoFile``
class uses the year, passed as a parameter, to update the values as required.

The years 1995, 2003, 2012 and 2016 have identical formatting so are used as the base, not the 1983 format.
"""

import dataclasses


@dataclasses.dataclass(kw_only=True)
class AMEReactionTwoLayout:
    """
    Storage class for the most common data in the AME reaction 2 data file.

    The AME reaction 2 data file is fixed-width file format so we will store the format details in this class.

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
    START_OneNeutronSeparationEnergy: int = 14
    END_OneNeutronSeparationEnergy: int = 22
    START_OneNeutronSeparationEnergyError: int = 23
    END_OneNeutronSeparationEnergyError: int = 30
    START_OneProtonSeparationEnergy: int = 32
    END_OneProtonSeparationEnergy: int = 40
    START_OneProtonSeparationEnergyError: int = 41
    END_OneProtonSeparationEnergyError: int = 48
    START_QFourBeta: int = 49
    END_QFourBeta: int = 58
    START_QFourBetaError: int = 59
    END_QFourBetaError: int = 66
    START_QDeuteronAlpha: int = 67
    END_QDeuteronAlpha: int = 76
    START_QDeuteronAlphaError: int = 77
    END_QDeuteronAlphaError: int = 84
    START_QProtonAlpha: int = 85
    END_QProtonAlpha: int = 94
    START_QProtonAlphaError: int = 95
    END_QProtonAlphaError: int = 102
    START_QNeutronAlpha: int = 103
    END_QNeutronAlpha: int = 112
    START_QNeutronAlphaError: int = 113
    END_QNeutronAlphaError: int = 125

    def __post_init__(self) -> None:
        self.columns: list[str] = [
            "A",
            "Z",
            "OneNeutronSeparationEnergy",
            "OneNeutronSeparationEnergyError",
            "OneProtonSeparationEnergy",
            "OneProtonSeparationEnergyError",
            "QFourBeta",
            "QFourBetaError",
            "QDeuteronAlpha",
            "QDeuteronAlphaError",
            "QProtonAlpha",
            "QProtonAlphaError",
            "QNeutronAlpha",
            "QNeutronAlphaError",
        ]

        self.positions: list[tuple[str, str, str]] = [(f"{c}", f"START_{c}", f"END_{c}") for c in self.columns]


class AMEReactionTwoFile:
    """
    Storage class for the year specific data in the AME reaction 2 data file.

    The base ``AMEReactionTwoLayout`` class is constructed and updated as required for the given ``year``.

    Parameters
    ----------
    year : int
        The year the file being parsed was published

    Attributes
    ----------
    YEAR_OVERRIDES : dict[int | str, dict[str, int]]
        Year specific updates and changes required to ``AMEReactionTwoLayout``.
    layout : AMEReactionTwoLayout
        A storage class containing details of parameters and their locations in the line.
    """

    YEAR_OVERRIDES: dict[int | str, dict[str, int]] = {
        "default": {},
        1983: {
            "HEADER": 30,
            "START_OneNeutronSeparationEnergyError": 24,
            "END_OneNeutronSeparationEnergyError": 28,
            "START_OneProtonSeparationEnergy": 30,
            "END_OneProtonSeparationEnergy": 40,
            "START_OneProtonSeparationEnergyError": 42,
            "END_OneProtonSeparationEnergyError": 48,
            "START_QFourBeta": 49,
            "END_QFourBeta": 57,
            "START_QFourBetaError": 60,
            "END_QFourBetaError": 65,
            "START_QDeuteronAlpha": 68,
            "END_QDeuteronAlpha": 76,
            "START_QDeuteronAlphaError": 78,
            "END_QDeuteronAlphaError": 84,
            "START_QProtonAlpha": 86,
            "END_QProtonAlpha": 94,
            "START_QProtonAlphaError": 96,
            "END_QProtonAlphaError": 102,
            "START_QNeutronAlpha": 103,
            "END_QNeutronAlpha": 112,
            "START_QNeutronAlphaError": 114,
            "END_QNeutronAlphaError": 120,
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
            "HEADER": 37,
            "FOOTER": 15,
            "END_OneNeutronSeparationEnergy": 24,
            "START_OneNeutronSeparationEnergyError": 25,
            "END_OneNeutronSeparationEnergyError": 34,
            "START_OneProtonSeparationEnergy": 36,
            "END_OneProtonSeparationEnergy": 46,
            "START_OneProtonSeparationEnergyError": 47,
            "END_OneProtonSeparationEnergyError": 56,
            "START_QFourBeta": 57,
            "END_QFourBeta": 68,
            "START_QFourBetaError": 69,
            "END_QFourBetaError": 78,
            "START_QDeuteronAlpha": 79,
            "END_QDeuteronAlpha": 90,
            "START_QDeuteronAlphaError": 91,
            "END_QDeuteronAlphaError": 100,
            "START_QProtonAlpha": 101,
            "END_QProtonAlpha": 112,
            "START_QProtonAlphaError": 113,
            "END_QProtonAlphaError": 122,
            "START_QNeutronAlpha": 123,
            "END_QNeutronAlpha": 134,
            "START_QNeutronAlphaError": 134,
            "END_QNeutronAlphaError": 144,
        },
    }

    def __init__(self, year: int) -> None:
        self.layout = AMEReactionTwoLayout(
            **AMEReactionTwoFile.YEAR_OVERRIDES.get(year, AMEReactionTwoFile.YEAR_OVERRIDES["default"])
        )
