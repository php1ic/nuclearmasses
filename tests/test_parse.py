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
    assert converter.normalise_symbol("H") == "H"
    assert converter.normalise_symbol("Os") == "Os"

    assert converter.normalise_symbol("h") == "H"
    assert converter.normalise_symbol("mg") == "Mg"
    assert converter.normalise_symbol("RN") == "Rn"
