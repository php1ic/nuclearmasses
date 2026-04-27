import pytest

from nuclearmasses.utils.converter import Converter


@pytest.fixture
def converter():
    return Converter()


def test_z_to_symbol(converter):
    assert converter.get_symbol(0) == "n"
    assert converter.get_symbol(6) == "C"
    assert converter.get_symbol(104) == "Rf"


def test_symbol_to_z(converter):
    assert converter.get_z("Al") == 13
    assert converter.get_z("Fe") == 26
    assert converter.get_z("Po") == 84


def test_normalise_symbol(converter):
    # These inputs shouldn't change
    assert converter.normalise_symbol("H") == "H"
    assert converter.normalise_symbol("Os") == "Os"

    # These inputs should change
    assert converter.normalise_symbol("h") == "H"
    assert converter.normalise_symbol("mg") == "Mg"
    assert converter.normalise_symbol("RN") == "Rn"


def test_units_to_seconds(converter):
    assert converter.unit_to_seconds("ms") == 1.0e-3
    assert converter.unit_to_seconds("s") == 1.0
    assert converter.unit_to_seconds("min") == 60.0
    assert converter.unit_to_seconds("h") == 3600.0
    assert converter.unit_to_seconds("d") == 86400.0
    assert converter.unit_to_seconds("yr") == 31557600.0


@pytest.mark.parametrize("unit", [5, "m", "Hz", "", "  "])
def test_nontime_unit_return_nan(converter, unit):
    assert converter.unit_to_seconds(unit) is None
