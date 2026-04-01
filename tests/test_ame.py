import importlib.resources

import pytest

from nuclearmasses.io.ame import AME


@pytest.fixture
def ame():
    data_path = importlib.resources.files("nuclearmasses.data")
    return AME(data_path=data_path)


def test_get_ame_datafiles(ame):
    year = 1983
    data_path = ame.data_path / str(year)
    mass, reaction01, reaction02 = ame.get_datafiles(year)
    assert mass == data_path / "mass.mas83"
    assert reaction01 == data_path / "rct1.mas83"
    assert reaction02 == data_path / "rct2.mas83"

    year = 1993
    data_path = ame.data_path / str(year)
    mass, reaction01, reaction02 = ame.get_datafiles(year)
    assert mass == data_path / "mass_exp.mas93"
    assert reaction01 == data_path / "rct1_exp.mas93"
    assert reaction02 == data_path / "rct2_exp.mas93"

    year = 1995
    data_path = ame.data_path / str(year)
    mass, reaction01, reaction02 = ame.get_datafiles(year)
    assert mass == data_path / "mass_exp.mas95"
    assert reaction01 == data_path / "rct1_exp.mas95"
    assert reaction02 == data_path / "rct2_exp.mas95"

    year = 2012
    data_path = ame.data_path / str(year)
    mass, reaction01, reaction02 = ame.get_datafiles(year)
    assert mass == data_path / "mass.mas12"
    assert reaction01 == data_path / "rct1.mas12"
    assert reaction02 == data_path / "rct2.mas12"

    year = 2016
    data_path = ame.data_path / str(year)
    mass, reaction01, reaction02 = ame.get_datafiles(year)
    assert mass == data_path / "mass16.txt"
    assert reaction01 == data_path / "rct1-16.txt"
    assert reaction02 == data_path / "rct2-16.txt"

    year = 2020
    data_path = ame.data_path / str(year)
    mass, reaction01, reaction02 = ame.get_datafiles(year)
    assert mass == data_path / "mass.mas20"
    assert reaction01 == data_path / "rct1.mas20"
    assert reaction02 == data_path / "rct2.mas20"
