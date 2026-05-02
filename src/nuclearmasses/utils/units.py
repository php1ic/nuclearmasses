"""
The module units contains functionality to convert from human readable strings into SI units. For example the time units
mins, hr or Gyr would be converted into seconds.
"""

UNIT_TO_SECONDS: dict[str, float] = {
    "ys": 1e-24,
    "zs": 1e-21,
    "as": 1e-18,
    "ps": 1e-12,
    "ns": 1e-9,
    "us": 1e-6,
    "ms": 1e-3,
    "s": 1.0,
    "min": 60.0,
    "h": 3600.0,
    "d": 86400.0,
    "yr": 31_557_600.0,  # 365.25 days
    "kyr": 3.15576e10,
    "tyr": 3.15576e12,
    "myr": 3.15576e13,
    "pyr": 3.15576e15,
    "gyr": 3.15576e16,
    "eyr": 3.15576e18,
    "zyr": 3.15576e21,
    "yyr": 3.15576e24,
}


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
    if not isinstance(unit_str, str):
        return None

    # Remove white space and make lower case to be consistent
    cleaned_unit = unit_str.strip().lower()
    if not cleaned_unit:
        return None

    return UNIT_TO_SECONDS.get(cleaned_unit, None)
