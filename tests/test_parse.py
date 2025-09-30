from nuclearmasses.element_converter import ElementConverter


def test_Z_to_symbol():
    converter = ElementConverter()

    assert converter.z_to_symbol[0] == "n"
    assert converter.z_to_symbol[6] == "C"
    assert converter.z_to_symbol[104] == "Rf"


def test_symbol_to_Z():
    converter = ElementConverter()

    assert converter.symbol_to_z["Al"] == 13
    assert converter.symbol_to_z["Fe"] == 26
    assert converter.symbol_to_z["Po"] == 84

