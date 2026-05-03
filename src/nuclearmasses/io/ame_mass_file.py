"""
The ame_mass_file module defines the ``AMEMassLayout`` and ``AMEMassFile`` classes. The ``AMEMassLayout`` class acts
like a base class, storing the common column names and the start and end positions of the values within the AME data
file. The positions change as time progress so the ``AMEMassFile`` class uses the year, passed as a parameter, to
update the values as required.

The years 2003, 2012 and 2016 have identical formatting so are used as the base, not the 1983 format.
"""

import dataclasses


@dataclasses.dataclass(kw_only=True)
class AMEMassLayout:
    """
    Storage class for the most common data in the AME mass data file.

    The AME mass data file is fixed-width file format so we will store the format details in this class.

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
    START_Z: int = 11
    END_Z: int = 14
    START_A: int = 16
    END_A: int = 19
    START_AMEMassExcess: int = 29
    END_AMEMassExcess: int = 41
    START_AMEMassExcessError: int = 42
    END_AMEMassExcessError: int = 53
    START_BindingEnergyPerA: int = 54
    END_BindingEnergyPerA: int = 64
    START_BindingEnergyPerAError: int = 65
    END_BindingEnergyPerAError: int = 72
    START_BetaDecayEnergy: int = 76
    END_BetaDecayEnergy: int = 86
    START_BetaDecayEnergyError: int = 87
    END_BetaDecayEnergyError: int = 95
    START_AtomicNumber: int = 96
    END_AtomicNumber: int = 99
    START_AtomicMass: int = 100
    END_AtomicMass: int = 112
    START_AtomicMassError: int = 113
    END_AtomicMassError: int = 120

    def __post_init__(self) -> None:
        self.columns: list[str] = [
            "Z",
            "A",
            "AMEMassExcess",
            "AMEMassExcessError",
            "BindingEnergyPerA",
            "BindingEnergyPerAError",
            "BetaDecayEnergy",
            "BetaDecayEnergyError",
            "AtomicNumber",
            "AtomicMass",
            "AtomicMassError",
        ]

        self.positions: list[tuple[str, str, str]] = [(f"{c}", f"START_{c}", f"END_{c}") for c in self.columns]


class AMEMassFile:
    """
    Storage class for the year specific data in the AME mass data file.

    The base ``AMEMassLayout`` class is constructed and updated as required for the given ``year``.

    Parameters
    ----------
    year : int
        The year the file being parsed was published

    Attributes
    ----------
    AME_MASS_YEAR_OVERRIDES : dict[int | str, dict[str, int]]
        Year specific updates and changes required to ``AMEMassLayout``.
    layout : AMEMassLayout
        A storage class containing details of parameters and their locations in the line.
    """

    AME_MASS_YEAR_OVERRIDES: dict[int | str, dict[str, int]] = {
        "default": {},
        1983: {
            "HEADER": 35,
            "END_AMEMassExcess": 39,
            "START_AMEMassExcessError": 41,
            "END_AMEMassExcessError": 48,
            "START_BindingEnergyPerA": 49,
            "END_BindingEnergyPerA": 59,
            "START_BindingEnergyPerAError": 61,
            "END_BindingEnergyPerAError": 68,
            "START_BetaDecayEnergy": 76,
            "END_BetaDecayEnergy": 85,
            "START_BetaDecayEnergyError": 87,
            "END_BetaDecayEnergyError": 94,
            "START_AtomicNumber": 97,
            "END_AtomicNumber": 99,
            "START_AtomicMass": 100,
            "END_AtomicMass": 110,
        },
        1993: {
            "HEADER": 40,
            "END_AMEMassExcess": 39,
            "START_AMEMassExcessError": 41,
            "END_AMEMassExcessError": 48,
            "START_BindingEnergyPerA": 49,
            "END_BindingEnergyPerA": 59,
            "START_BindingEnergyPerAError": 61,
            "END_BindingEnergyPerAError": 68,
            "START_BetaDecayEnergy": 76,
            "END_BetaDecayEnergy": 85,
            "START_BetaDecayEnergyError": 87,
            "END_BetaDecayEnergyError": 94,
            "START_AtomicNumber": 97,
            "END_AtomicNumber": 99,
            "START_AtomicMass": 100,
            "END_AtomicMass": 110,
            "START_AtomicMassError": 112,
        },
        1995: {
            "END_AMEMassExcess": 39,
            "START_AMEMassExcessError": 41,
            "END_AMEMassExcessError": 48,
            "START_BindingEnergyPerA": 49,
            "END_BindingEnergyPerA": 59,
            "START_BindingEnergyPerAError": 61,
            "END_BindingEnergyPerAError": 68,
            "START_BetaDecayEnergy": 76,
            "END_BetaDecayEnergy": 85,
            "START_BetaDecayEnergyError": 87,
            "END_BetaDecayEnergyError": 94,
            "START_AtomicNumber": 97,
            "END_AtomicNumber": 99,
            "START_AtomicMass": 100,
            "END_AtomicMass": 110,
            "START_AtomicMassError": 112,
        },
        # The years 2003, 2012 and 2016 have identical formatting so are used as the base
        2003: {},
        2012: {},
        2016: {},
        2020: {
            "HEADER": 36,
            "END_AMEMassExcess": 42,
            "START_AMEMassExcessError": 43,
            "END_AMEMassExcessError": 53,
            "START_BindingEnergyPerA": 56,
            "END_BindingEnergyPerA": 66,
            "START_BindingEnergyPerAError": 69,
            "END_BindingEnergyPerAError": 77,
            "START_BetaDecayEnergy": 82,
            "END_BetaDecayEnergy": 93,
            "START_BetaDecayEnergyError": 95,
            "END_BetaDecayEnergyError": 104,
            "START_AtomicNumber": 106,
            "END_AtomicNumber": 109,
            "START_AtomicMass": 110,
            "END_AtomicMass": 120,
            "START_AtomicMassError": 124,
            "END_AtomicMassError": 135,
        },
    }

    def __init__(self, year: int) -> None:
        self.layout = AMEMassLayout(
            **AMEMassFile.AME_MASS_YEAR_OVERRIDES.get(year, AMEMassFile.AME_MASS_YEAR_OVERRIDES["default"])
        )
