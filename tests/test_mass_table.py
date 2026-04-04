import pandas as pd
import pandas.testing as pdt
import pytest

from nuclearmasses.mass_table import MassTable


@pytest.fixture
def empty_frame():
    return MassTable(df=pd.DataFrame())


def test_initial_complete_parse():
    data = MassTable().df
    expected_shape = (21421, 50)

    assert expected_shape == data.shape


def test_getter_creation():
    cols = ["Mass", "Error", "Param", "RandomLongerString"]
    test_frame = pd.DataFrame.from_dict(data=dict.fromkeys(cols, [0]))

    df = MassTable(df=test_frame)

    for name in cols:
        f = f"get_{name}"
        assert hasattr(df, f)
        assert callable(getattr(df, f))


def test_getter_not_created(empty_frame):
    with pytest.raises(AttributeError):
        empty_frame.get_Nothing()


def test_empty_filter(empty_frame):
    assert len(empty_frame._filters) == 0


def test_manually_populated_filter():
    cols = ["ManualParameter"]
    test_frame = pd.DataFrame.from_dict(data=dict.fromkeys(cols, [0]))

    my_filter = [(cols[0], "==", 5)]

    df = MassTable(df=test_frame, filters=my_filter)

    assert len(df._filters) == 1
    assert df._filters == my_filter


def test_auto_populated_filter():
    cols = ["AutoParameter"]
    test_frame = pd.DataFrame.from_dict(data=dict.fromkeys(cols, [0]))

    df = MassTable(df=test_frame)

    val = 2
    f_df = df.get_AutoParameter(val)

    assert len(f_df._filters) == 1
    assert f_df._filters == [(cols[0], "==", val)]


def test_getter_on_index():
    cols = ["Mass", "Error", "Param", "RandomLongerString"]
    test_frame = pd.DataFrame.from_dict(data=dict.fromkeys(cols, [0]))

    m_df = MassTable(df=test_frame)
    m_df.set_index("Param")
    m_df = m_df.get_Param(0).df

    expected = pd.DataFrame(
        {
            "Mass": [0],
            "Error": [0],
            "Param": [0],
            "RandomLongerString": [0],
        }
    )

    pdt.assert_frame_equal(m_df, expected, check_like=True)


def test_access_property():
    cols = ["Mass", "Error", "Param", "RandomLongerString"]
    test_frame = pd.DataFrame.from_dict(data=dict.fromkeys(cols, [0]))

    m_df = MassTable(df=test_frame).df

    expected = pd.DataFrame(
        {
            "Mass": [0],
            "Error": [0],
            "Param": [0],
            "RandomLongerString": [0],
        }
    )

    pdt.assert_frame_equal(m_df, expected, check_like=True)


def test_generic_getter():
    cols = ["Mass", "Error", "Param", "RandomLongerString"]
    test_frame = pd.DataFrame.from_dict(data=dict.fromkeys(cols, [0]))

    m_df = MassTable(df=test_frame).get("Error", 0).df

    expected = pd.DataFrame(
        {
            "Mass": [0],
            "Error": [0],
            "Param": [0],
            "RandomLongerString": [0],
        }
    )

    pdt.assert_frame_equal(m_df, expected, check_like=True)


def test_generic_filter():
    cols = ["Mass", "Error", "Param", "RandomLongerString"]
    test_frame = pd.DataFrame.from_dict(data=dict.fromkeys(cols, [0]))

    m_df = MassTable(df=test_frame).filter("Param == 0").df

    expected = pd.DataFrame(
        {
            "Mass": [0],
            "Error": [0],
            "Param": [0],
            "RandomLongerString": [0],
        }
    )

    pdt.assert_frame_equal(m_df, expected, check_like=True)
