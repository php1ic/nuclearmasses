from nuclearmasses.ame_reaction_1_parse import AMEReactionParserOne

import io
import pandas as pd
import pandas.testing as pdt


def test_read_line():
    # We are cheating a little here because this line does not have the A value in the file
    # To test properly either choose a different isotope or read from the first instance with A so it gets populated
    line = io.StringIO(" 186 Ir  77   15780     250      9536      20      3850     100     -7600#    300#    -2639      20    -10640#    200#")
    parser = AMEReactionParserOne(line, 1983)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
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

    line = io.StringIO(" 186 Ir  77   15704.74   32.47   9524.26   17.08   3849.65  103.31  -7458.10   26.70  -2639.77   16.57 -10561.10   44.19")
    parser = AMEReactionParserOne(line, 2003)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
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

    line = io.StringIO(" 186 Ir  77   15706.55   32.47   9527.99   17.09   3848.03  103.31  -7459.92   26.70  -2641.13   16.57 -10557.95   30.67")
    parser = AMEReactionParserOne(line, 2012)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
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

    line = io.StringIO(" 186 Ir  77   15704.13   32.47   9530.65   17.07   3848.80  103.31  -7457.49   26.70  -2642.29   16.55 -10555.52   30.67")
    parser = AMEReactionParserOne(line, 2016)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
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

    line = io.StringIO(" 186 Ir  77   15704.1312   32.4655   9530.4731   17.0698   3848.8777  103.3133  -7457.4943   26.6968  -2642.2739   16.5459 -10555.5245   30.6658")
    parser = AMEReactionParserOne(line, 2020)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
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
