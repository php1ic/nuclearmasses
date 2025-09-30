from nuclearmasses.ame_reaction_1_parse import AMEReactionParserOne

import io
import pandas as pd
import pandas.testing as pdt


def test_1983_rct1():
    # We are cheating a little here because this line does not have the A value in the file
    # To test properly either choose a different isotope or read from the first instance with A so it gets populated
    line = io.StringIO(" 186 Ir  77   15780     250      9536      20      3850     100     -7600#    300#    -2639      20    -10640#    200#")
    parser = AMEReactionParserOne(line, 1983)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
        'TableYear': [1983],
        'Symbol': ['Ir'],
        'A': [186],
        'Z': [77],
        'N': [109],
        'TwoNeutronSeparationEnergy': [15780],
        'TwoNeutronSeparationEnergyError': [250],
        'TwoProtonSeparationEnergy': [9536],
        'TwoProtonSeparationEnergyError': [20],
        'QAlpha': [3850],
        'QAlphaError': [100],
        'QTwoBeta': [-7600],
        'QTwoBetaError': [300],
        'QEpsilon': [-2639],
        'QEpsilonError': [20],
        'QBetaNeutron': [-10640],
        'QBetaNeutronError': [200],
    })
    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)


def test_1993_rct1():
    line = io.StringIO(" 186 Ir  77   15618.44  270.74   9522.98   20.49   3852.98  103.94  -7419.61  145.57  -2635.85   20.03 -10622#    230#")
    parser = AMEReactionParserOne(line, 1993)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
        'TableYear': [1993],
        'Symbol': ['Ir'],
        'A': [186],
        'Z': [77],
        'N': [109],
        'TwoNeutronSeparationEnergy': [15618.44],
        'TwoNeutronSeparationEnergyError': [270.74],
        'TwoProtonSeparationEnergy': [9522.89],
        'TwoProtonSeparationEnergyError': [20.49],
        'QAlpha': [3852.98],
        'QAlphaError': [103.94],
        'QTwoBeta': [-7419.61],
        'QTwoBetaError': [145.57],
        'QEpsilon': [-2635.85],
        'QEpsilonError': [20.03],
        'QBetaNeutron': [-10622],
        'QBetaNeutronError': [230],
    })
    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)


def test_1995_rct1():
    line = io.StringIO(" 186 Ir  77   15618.41  270.74   9522.89   20.49   3853.04  103.94  -7495.33  145.56  -2635.83   20.03 -10682.00  207.60")
    parser = AMEReactionParserOne(line, 1995)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
        'TableYear': [1995],
        'Symbol': ['Ir'],
        'A': [186],
        'Z': [77],
        'N': [109],
        'TwoNeutronSeparationEnergy': [15618.41],
        'TwoNeutronSeparationEnergyError': [270.74],
        'TwoProtonSeparationEnergy': [9522.89],
        'TwoProtonSeparationEnergyError': [20.49],
        'QAlpha': [3853.04],
        'QAlphaError': [103.94],
        'QTwoBeta': [-7495.33],
        'QTwoBetaError': [145.56],
        'QEpsilon': [-2635.83],
        'QEpsilonError': [20.03],
        'QBetaNeutron': [-10682.00],
        'QBetaNeutronError': [207.60],
    })
    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)


def test_2003_rct1():
    line = io.StringIO(" 186 Ir  77   15704.74   32.47   9524.26   17.08   3849.65  103.31  -7458.10   26.70  -2639.77   16.57 -10561.10   44.19")
    parser = AMEReactionParserOne(line, 2003)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
        'TableYear': [2003],
        'Symbol': ['Ir'],
        'A': [186],
        'Z': [77],
        'N': [109],
        'TwoNeutronSeparationEnergy': [15704.74],
        'TwoNeutronSeparationEnergyError': [32.47],
        'TwoProtonSeparationEnergy': [9524.26],
        'TwoProtonSeparationEnergyError': [17.08],
        'QAlpha': [3849.65],
        'QAlphaError': [103.31],
        'QTwoBeta': [-7458.10],
        'QTwoBetaError': [26.70],
        'QEpsilon': [-2639.77],
        'QEpsilonError': [16.57],
        'QBetaNeutron': [-10561.10],
        'QBetaNeutronError': [44.19],
    })
    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)


def test_2012_rct1():
    line = io.StringIO(" 186 Ir  77   15706.55   32.47   9527.99   17.09   3848.03  103.31  -7459.92   26.70  -2641.13   16.57 -10557.95   30.67")
    parser = AMEReactionParserOne(line, 2012)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
        'TableYear': [2012],
        'Symbol': ['Ir'],
        'A': [186],
        'Z': [77],
        'N': [109],
        'TwoNeutronSeparationEnergy': [15706.55],
        'TwoNeutronSeparationEnergyError': [32.47],
        'TwoProtonSeparationEnergy': [9527.99],
        'TwoProtonSeparationEnergyError': [17.09],
        'QAlpha': [3848.03],
        'QAlphaError': [103.31],
        'QTwoBeta': [-7459.92],
        'QTwoBetaError': [26.70],
        'QEpsilon': [-2641.13],
        'QEpsilonError': [16.57],
        'QBetaNeutron': [-10557.95],
        'QBetaNeutronError': [30.67],
    })
    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)


def test_2016_rct1():
    line = io.StringIO(" 186 Ir  77   15704.13   32.47   9530.65   17.07   3848.80  103.31  -7457.49   26.70  -2642.29   16.55 -10555.52   30.67")
    parser = AMEReactionParserOne(line, 2016)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
        'TableYear': [2016],
        'Symbol': ['Ir'],
        'A': [186],
        'Z': [77],
        'N': [109],
        'TwoNeutronSeparationEnergy': [15704.13],
        'TwoNeutronSeparationEnergyError': [32.47],
        'TwoProtonSeparationEnergy': [9530.65],
        'TwoProtonSeparationEnergyError': [17.07],
        'QAlpha': [3848.80],
        'QAlphaError': [103.31],
        'QTwoBeta': [-7457.49],
        'QTwoBetaError': [26.70],
        'QEpsilon': [-2642.29],
        'QEpsilonError': [16.55],
        'QBetaNeutron': [-10555.52],
        'QBetaNeutronError': [30.67],
    })
    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)


def test_2020_rct1():
    line = io.StringIO(" 186 Ir  77   15704.1312   32.4655   9530.4731   17.0698   3848.8777  103.3133  -7457.4943   26.6968  -2642.2739   16.5459 -10555.5245   30.6658")
    parser = AMEReactionParserOne(line, 2020)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
        'TableYear': [2020],
        'Symbol': ['Ir'],
        'A': [186],
        'Z': [77],
        'N': [109],
        'TwoNeutronSeparationEnergy': [15704.1312],
        'TwoNeutronSeparationEnergyError': [32.4655],
        'TwoProtonSeparationEnergy': [9530.4731],
        'TwoProtonSeparationEnergyError': [17.0698],
        'QAlpha': [3848.8777],
        'QAlphaError': [103.3133],
        'QTwoBeta': [-7457.4943],
        'QTwoBetaError': [26.6968],
        'QEpsilon': [-2642.2739],
        'QEpsilonError': [16.5459],
        'QBetaNeutron': [-10555.5245],
        'QBetaNeutronError': [30.6658],
    })
    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)
