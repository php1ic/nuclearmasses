from nuclearmasses.utils.dataframe_utils import calculate_relative_error, strip_char_from_string_columns

import pandas as pd


def test_12C_relative_error():
    df = pd.DataFrame(
        {
            "A": [12],
            "Z": [6],
            "NUBASEMassExcess": [-12345.6],
            "NUBASEMassExcessError": [1.2],
        }
    )

    df = calculate_relative_error(df, "NUBASE")
    assert df["NUBASERelativeError"][0] == 0.0


def test_relative_error():
    df = pd.DataFrame(
        {
            "A": [123],
            "Z": [50],
            "NUBASEMassExcess": [100000.0],
            "NUBASEMassExcessError": [10.0],
        }
    )

    df = calculate_relative_error(df, "NUBASE")
    assert df["NUBASERelativeError"][0] == 10.0/100000.0


def test_remove_hash_from_column():
    df = pd.DataFrame(
        {
            "X": ["Random#"],
            "Y": ["Clean"],
        }
    )

    df = strip_char_from_string_columns(df, "#")
    assert df["X"][0] == "Random"
    assert df["Y"][0] == "Clean"


def test_remove_decimal_from_column():
    df = pd.DataFrame(
        {
            "X": ["Random.String"],
            "Y": ["Clean"],
        }
    )

    df = strip_char_from_string_columns(df, ".")
    assert df["X"][0] == "RandomString"
    assert df["Y"][0] == "Clean"
