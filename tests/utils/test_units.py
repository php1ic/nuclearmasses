import pytest

from nuclearmasses.utils.units import unit_to_seconds


def test_units_to_seconds():
    assert unit_to_seconds("ms") == 1.0e-3
    assert unit_to_seconds("s") == 1.0
    assert unit_to_seconds("min") == 60.0
    assert unit_to_seconds("h") == 3600.0
    assert unit_to_seconds("d") == 86400.0
    assert unit_to_seconds("yr") == 31557600.0


@pytest.mark.parametrize("unit", [5, "m", "Hz", "", "  "])
def test_nontime_unit_return_nan(unit):
    assert unit_to_seconds(unit) is None
