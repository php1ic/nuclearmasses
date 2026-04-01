import importlib.resources

import pytest

from nuclearmasses.io.nubase import NUBASE


@pytest.fixture
def nubase():
    data_path = importlib.resources.files("nuclearmasses.data")
    return NUBASE(data_path=data_path)


def test_get_nubase_datafile(nubase):
    year = 1995
    assert nubase.get_datafile(year) == nubase.data_path / str(year) / "nubtab97.asc"
    year = 2003
    assert nubase.get_datafile(year) == nubase.data_path / str(year) / "nubtab03.asc"
    year = 2012
    assert nubase.get_datafile(year) == nubase.data_path / str(year) / "nubtab12.asc"
    year = 2016
    assert nubase.get_datafile(year) == nubase.data_path / str(year) / "nubase2016.txt"
    year = 2020
    assert nubase.get_datafile(year) == nubase.data_path / str(year) / "nubase_1.mas20"
