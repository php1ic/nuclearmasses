from nuclearmasses.mass_table import MassTable


def test_get_nubase_datafile():
    mt = MassTable()

    year = 1995
    assert mt._get_nubase_datafile(year) == mt.data_path / str(year) / "nubtab97.asc"
    year = 2003
    assert mt._get_nubase_datafile(year) == mt.data_path / str(year) / "nubtab03.asc"
    year = 2012
    assert mt._get_nubase_datafile(year) == mt.data_path / str(year) / "nubtab12.asc"
    year = 2016
    assert mt._get_nubase_datafile(year) == mt.data_path / str(year) / "nubase2016.txt"
    year = 2020
    assert mt._get_nubase_datafile(year) == mt.data_path / str(year) / "nubase_1.mas20"


def test_get_ame_datafiles():
    mt = MassTable()

    year = 1983
    data_path = mt.data_path / str(year)
    mass, reaction01, reaction02 = mt._get_ame_datafiles(1983)
    assert mass == data_path / "mass.mas83"
    assert reaction01 == data_path / "rct1.mas83"
    assert reaction02 == data_path / "rct2.mas83"

    year = 1993
    data_path = mt.data_path / str(year)
    mass, reaction01, reaction02 = mt._get_ame_datafiles(1993)
    assert mass == data_path / "mass_exp.mas93"
    assert reaction01 == data_path / "rct1_exp.mas93"
    assert reaction02 == data_path / "rct2_exp.mas93"

    year = 1995
    data_path = mt.data_path / str(year)
    mass, reaction01, reaction02 = mt._get_ame_datafiles(1995)
    assert mass == data_path / "mass_exp.mas95"
    assert reaction01 == data_path / "rct1_exp.mas95"
    assert reaction02 == data_path / "rct2_exp.mas95"

    year = 2012
    data_path = mt.data_path / str(year)
    mass, reaction01, reaction02 = mt._get_ame_datafiles(2012)
    assert mass == data_path / "mass.mas12"
    assert reaction01 == data_path / "rct1.mas12"
    assert reaction02 == data_path / "rct2.mas12"

    year = 2016
    data_path = mt.data_path / str(year)
    mass, reaction01, reaction02 = mt._get_ame_datafiles(2016)
    assert mass == data_path / "mass16.txt"
    assert reaction01 == data_path / "rct1-16.txt"
    assert reaction02 == data_path / "rct2-16.txt"

    year = 2020
    data_path = mt.data_path / str(year)
    mass, reaction01, reaction02 = mt._get_ame_datafiles(2020)
    assert mass == data_path / "mass.mas20"
    assert reaction01 == data_path / "rct1.mas20"
    assert reaction02 == data_path / "rct2.mas20"
