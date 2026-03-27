from nuclearmasses.utils.converter import Converter


def test_z_to_symbol():
    converter = Converter()

    assert converter.get_symbol(0) == "n"
    assert converter.get_symbol(6) == "C"
    assert converter.get_symbol(104) == "Rf"


def test_symbol_to_z():
    converter = Converter()

    assert converter.get_z("Al") == 13
    assert converter.get_z("Fe") == 26
    assert converter.get_z("Po") == 84
