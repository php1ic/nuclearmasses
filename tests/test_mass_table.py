from nuclearmasses.mass_table import MassTable


def test_initial_complete_parse():
    data = MassTable().data
    expected_shape = (21421, 50)

    assert expected_shape == data.shape
