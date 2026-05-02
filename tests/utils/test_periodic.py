from nuclearmasses.utils.periodic import get_symbol, get_z, normalise_symbol


def test_z_to_symbol():
    assert get_symbol(0) == "n"
    assert get_symbol(6) == "C"
    assert get_symbol(104) == "Rf"


def test_symbol_to_z():
    assert get_z("Al") == 13
    assert get_z("Fe") == 26
    assert get_z("Po") == 84


def test_normalise_symbol():
    # These inputs shouldn't change
    assert normalise_symbol("H") == "H"
    assert normalise_symbol("Os") == "Os"

    # These inputs should change
    assert normalise_symbol("h") == "H"
    assert normalise_symbol("mg") == "Mg"
    assert normalise_symbol("RN") == "Rn"

