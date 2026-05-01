"""
The nubase_file module defines the ``NUBASELayout`` and ``NUBASEFile`` classes. The ``NUBASELayout`` class acts like a
base class, storing the original column names and the start and end positionsof the values within the NUBASE data file.
The positions change as time progress so the ``NUBASEFile`` class uses the year, passed as a parameter, to update the
values as required.
"""

import dataclasses


@dataclasses.dataclass(kw_only=True)
class NUBASELayout:
    """
    Storage class for the original data in the NUBASE data file.

    The NUBASE data file is fixed-width file format so we will store the format details in this class.

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
        The first column of parameter X or None if X is not in the datafile for that year.
    END_X : int or None
        The last column of parameter X or None if X is not in the datafile for that year.
    columns : list[str]
        The list of columns that appear in the file.
    positions : list[tuple(str, str, str)]
        A list of tuples detailing column name alongside start and end position in the line.
    """

    HEADER: int = 0
    FOOTER: int = 0
    START_A: int = 0
    END_A: int = 3
    START_Z: int = 4
    END_Z: int = 7
    START_State: int = 7
    END_State: int = 8
    START_NUBASEMassExcess: int = 18
    END_NUBASEMassExcess: int = 29
    START_NUBASEMassExcessError: int = 29
    END_NUBASEMassExcessError: int = 38
    START_IsomerEnergy: int = 39
    END_IsomerEnergy: int = 46
    START_IsomerEnergyError: int = 48
    END_IsomerEnergyError: int = 56
    START_HalfLifeValue: int = 60
    END_HalfLifeValue: int = 68
    START_HalfLifeUnit: int = 69
    END_HalfLifeUnit: int = 71
    START_HalfLifeError: int = 72
    END_HalfLifeError: int = 77
    START_Spin: int = 79
    END_Spin: int = 93
    START_DecayModes: int = 106
    END_DecayModes: int | None = None

    # Columns that weren't in the first file so are not part of the default
    START_DiscoveryYear: int | None = None
    END_DiscoveryYear: int | None = None
    START_ENSDF: int | None = None
    END_ENSDF: int | None = None

    def __post_init__(self) -> None:
        self.columns: list[str] = [
            "A",
            "Z",
            "State",
            "NUBASEMassExcess",
            "NUBASEMassExcessError",
            "IsomerEnergy",
            "IsomerEnergyError",
            "HalfLifeValue",
            "HalfLifeUnit",
            "HalfLifeError",
            "Spin",
            # "ENSDF",
            # "DiscoveryYear",
            "DecayModes",
        ]

        self.positions: list[tuple[str, str, str]] = [(f"{c}", f"START_{c}", f"END_{c}") for c in self.columns]


class NUBASEFile:
    """
    Storage class for the year specific data in the NUBASE data file.

    The base ``NUBASELayout`` class is constructed and updated as required for the given ``year``.

    Parameters
    ----------
    year : int
        The year the file being parsed was published

    Attributes
    ----------
    NUBASE_YEAR_OVERRIDES : dict[int | str, dict[str, int]]
        Year specific updates and changes required to ``NUBASELayout``.
    layout : NUBASELayout
        A storage class containing details of parameters and their locations in the line.
    """

    NUBASE_YEAR_OVERRIDES: dict[int | str, dict[str, int]] = {
        "default": {},  # Use this to appease mypy by not returning None for a non-existent value
        # Original columns and their positions are based of the 1995 file
        1995: {},
        # No changes in 2000
        2003: {},
        # New discovery year column in 2012 which pushed the decay modes to the right
        2012: {
            "START_DiscoveryYear": 105,
            "END_DiscoveryYear": 109,
            "START_DecayModes": 110,
        },
        # This is the same as 2012 and copy pasting seems to be the simplest way to have the same values
        2016: {
            "START_DiscoveryYear": 105,
            "END_DiscoveryYear": 109,
            "START_DecayModes": 110,
        },
        # Big update in 2020
        #    Added a header block
        #    Increased total digits in various values, pushing almost all columns to the right
        #    New column representing the year isotopes details were last updated in ENSDF
        2020: {
            "HEADER": 25,
            "START_NUBASEMassExcessError": 31,
            "END_NUBASEMassExcessError": 42,
            "START_IsomerEnergy": 43,
            "END_IsomerEnergy": 53,
            "START_IsomerEnergyError": 54,
            "END_IsomerEnergyError": 64,
            "START_HalfLifeValue": 69,
            "END_HalfLifeValue": 77,
            "START_HalfLifeUnit": 78,
            "END_HalfLifeUnit": 80,
            "START_HalfLifeError": 81,
            "END_HalfLifeError": 87,
            "START_Spin": 88,
            "END_Spin": 101,
            "START_ENSDF": 102,
            "END_ENSDF": 103,
            "START_DiscoveryYear": 114,
            "END_DiscoveryYear": 118,
            "START_DecayModes": 119,
        },
    }

    def __init__(self, year: int) -> None:
        self.layout = NUBASELayout(
            **NUBASEFile.NUBASE_YEAR_OVERRIDES.get(year, NUBASEFile.NUBASE_YEAR_OVERRIDES["default"])
        )
