from nuclearmasses.nubase_parse import NUBASEParser

import io
import pandas as pd
import pandas.testing as pdt


def test_1995_nubase():
    line = io.StringIO("168 0670   168Ho  -60085       29                              2.99   m 0.07   3+            94           B-=100")
    parser = NUBASEParser(line, 1995)
    df = parser.read_file()

    expected = pd.DataFrame({
        'TableYear': [1995],
        'Experimental': [True],
        'Symbol': ['Ho'],
        'A': [168],
        'Z': [67],
        'N': [101],
        'NUBASEMassExcess': [-60085],
        'NUBASEMassExcessError': [29],
        'HalfLifeValue': [2.99],
        'HalfLifeUnit': ['m'],
        'HalfLifeError': [0.07],
        'Spin': ['3+'],
        'DecayModes': ['B-=100'],
        })

    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)


def test_2003_nubase():
    line = io.StringIO("168 0670   168Ho  -60070       30                              2.99   m 0.07   3+            94           B-=100")
    parser = NUBASEParser(line, 2003)
    df = parser.read_file()

    expected = pd.DataFrame({
        'TableYear': [2003],
        'Experimental': [True],
        'Symbol': ['Ho'],
        'A': [168],
        'Z': [67],
        'N': [101],
        'NUBASEMassExcess': [-60070],
        'NUBASEMassExcessError': [30],
        'HalfLifeValue': [2.99],
        'HalfLifeUnit': ['m'],
        'HalfLifeError': [0.07],
        'Spin': ['3+'],
        'DecayModes': ['B-=100'],
        })

    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)


def test_2012_nubase():
    line = io.StringIO("168 0670   168Ho  -60060       30                              2.99   m 0.07   3+            10          1960 B-=100")
    parser = NUBASEParser(line, 2012)
    df = parser.read_file()

    expected = pd.DataFrame({
        'TableYear': [2012],
        'Experimental': [True],
        'Symbol': ['Ho'],
        'A': [168],
        'Z': [67],
        'N': [101],
        'NUBASEMassExcess': [-60060],
        'NUBASEMassExcessError': [30],
        'HalfLifeValue': [2.99],
        'HalfLifeUnit': ['m'],
        'HalfLifeError': [0.07],
        'Spin': ['3+'],
        'DiscoveryYear': [1960],
        'DecayModes': ['B-=100'],
        })

    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)


def test_2016_nubase():
    line = io.StringIO("168 0670   168Ho  -60060       30                              2.99   m 0.07   3+            10          1960 B-=100")
    parser = NUBASEParser(line, 2016)
    df = parser.read_file()

    expected = pd.DataFrame({
        'TableYear': [2016],
        'Experimental': [True],
        'Symbol': ['Ho'],
        'A': [168],
        'Z': [67],
        'N': [101],
        'NUBASEMassExcess': [-60060],
        'NUBASEMassExcessError': [30],
        'HalfLifeValue': [2.99],
        'HalfLifeUnit': ['m'],
        'HalfLifeError': [0.07],
        'Spin': ['3+'],
        'DiscoveryYear': [1960],
        'DecayModes': ['B-=100'],
        })

    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)


def test_2020_nubase():
    line = io.StringIO("168 0670   168Ho  -60060         30                                     2.99   m 0.07   3+            10          1960 B-=100")
    parser = NUBASEParser(line, 2020)
    parser.HEADER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
        'TableYear': [2020],
        'Experimental': [True],
        'Symbol': ['Ho'],
        'A': [168],
        'Z': [67],
        'N': [101],
        'NUBASEMassExcess': [-60060],
        'NUBASEMassExcessError': [30],
        'HalfLifeValue': [2.99],
        'HalfLifeUnit': ['m'],
        'HalfLifeError': [0.07],
        'Spin': ['3+'],
        'DiscoveryYear': [1960],
        'DecayModes': ['B-=100'],
        })

    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)
