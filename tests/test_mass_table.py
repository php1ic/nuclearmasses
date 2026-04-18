import pytest

from nuclearmasses.mass_table import MassTable


@pytest.fixture
def the_table():
    return MassTable()


def test_initial_complete_parse(the_table):
    expected_shape = (21421, 51)
    assert expected_shape == the_table.data.shape


def test_valid_user_data(the_table):
    data = '[{"A": 5, "Z": 2, "AMEMassExcess": 123456.7}]'
    the_table.add_user_data(data)
    df = the_table.data
    assert (21422, 51) == df.shape
    assert df[(df["A"] == 5) & (df["Z"] == 2) & (df["DataSource"] == 1)]["AMEMassExcess"].iloc[0] == 123456.7


def test_common_value_user_data(the_table):
    data = '[{"A": 5, "Z": 2, "AMEMassExcess": 123456.7}]'
    common_val = {"TableYear": 2099}
    the_table.add_user_data(data, common_values=common_val)
    df = the_table.data
    assert (21422, 51) == df.shape
    assert df[(df["A"] == 5) & (df["Z"] == 2) & (df["DataSource"] == 1)]["TableYear"].iloc[0] == 2099


def test_missing_column_user_data(the_table):
    data = '[{"Z": 2, "AMEMassExcess": 123456.7}]'
    with pytest.raises(ValueError, match="ERROR: Missing required columns:.*A.*"):
        the_table.add_user_data(data)


def test_typo_column_user_data(the_table):
    data = '[{"A": 5, "Z": 2, "AMEMassexcess": 123456.7}]'
    with pytest.raises(ValueError, match="ERROR: Column.*not recognised. Did you mean.*?"):
        the_table.add_user_data(data)


def test_invalid_column_user_data(the_table):
    data = '[{"A": 5, "Z": 2, "MadeUpColumn": 123456.7}]'
    with pytest.raises(ValueError, match="ERROR: Column.*not recognised."):
        the_table.add_user_data(data)


def test_na_column_user_data(the_table):
    data = '[{"A": 5, "Z": NaN, "AMEMassExcess": 123456.7}]'
    with pytest.raises(ValueError, match="Required columns have missing values."):
        the_table.add_user_data(data)


def test_duplicate_row_user_data(the_table):
    data = '[{"A": 5, "Z": 2, "AMEMassExcess": 123456.7},{"A": 5, "Z": 2, "AMEMassExcess": 123456.7}]'
    with pytest.raises(ValueError, match="Duplicate rows, will not guess which should be used."):
        the_table.add_user_data(data)
