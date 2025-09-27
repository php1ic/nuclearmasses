from nuclearmasses.ame_reaction_2_parse import AMEReactionParserTwo

import io
import pandas as pd
import pandas.testing as pdt


def test_read_line():
    line = io.StringIO(" 204 Tl  81    7853      17      5702.8     1.7  -13480     120     12613.7     1.8    8608.4     1.8    7180      50")
    parser = AMEReactionParserTwo(line, 1983)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
        'Symbol': ['Tl'],
        'A': [204],
        'Z': [81],
        'N': [123],
        'OneNeutronSeparationEnergy': [7853],
        'OneNeutronSeparationEnergyError': [17],
        'OneProtonSeparationEnergy': [5702.8],
        'OneProtonSeparationEnergyError': [1.7],
        'QFourBeta': [-13480],
        'QFourBetaError': [120],
        'QDeuteronAlpha': [12613.7],
        'QDeuteronAlphaError': [1.8],
        'QProtonAlpha': [8608.4],
        'QProtonAlphaError': [1.8],
        'QNeutronAlpha': [7180],
        'QNeutronAlphaError': [50],
    })

    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)

    line = io.StringIO(" 204 Tl  81    6656.10    0.29   6365.82    1.25 -12470.66   24.01  13710.69    1.15   8181.34    1.16   7701.54    3.34")
    parser = AMEReactionParserTwo(line, 2003)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
        'Symbol': ['Tl'],
        'A': [204],
        'Z': [81],
        'N': [123],
        'OneNeutronSeparationEnergy': [6656.10],
        'OneNeutronSeparationEnergyError': [0.29],
        'OneProtonSeparationEnergy': [6365.82],
        'OneProtonSeparationEnergyError': [1.25],
        'QFourBeta': [-12470.66],
        'QFourBetaError': [24.01],
        'QDeuteronAlpha': [13710.69],
        'QDeuteronAlphaError': [1.15],
        'QProtonAlpha': [8181.34],
        'QProtonAlphaError': [1.16],
        'QNeutronAlpha': [7701.54],
        'QNeutronAlphaError': [3.34],
    })

    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)

    line = io.StringIO(" 204 Tl  81    6656.09    0.29   6365.80    1.25 -12470.19   22.31  13710.68    1.14   8181.16    1.15   7701.67    3.33")
    parser = AMEReactionParserTwo(line, 2012)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
        'Symbol': ['Tl'],
        'A': [204],
        'Z': [81],
        'N': [123],
        'OneNeutronSeparationEnergy': [6656.09],
        'OneNeutronSeparationEnergyError': [0.29],
        'OneProtonSeparationEnergy': [6365.80],
        'OneProtonSeparationEnergyError': [1.25],
        'QFourBeta': [-12470.19],
        'QFourBetaError': [22.31],
        'QDeuteronAlpha': [13710.68],
        'QDeuteronAlphaError': [1.14],
        'QProtonAlpha': [8181.16],
        'QProtonAlphaError': [1.15],
        'QNeutronAlpha': [7701.67],
        'QNeutronAlphaError': [3.33],
    })

    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)

    line = io.StringIO(" 204 Tl  81    6656.08    0.29   6365.85    1.25 -12470.71   22.32  13709.99    1.06   8180.45    1.07   7700.97    3.31")
    parser = AMEReactionParserTwo(line, 2016)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
        'Symbol': ['Tl'],
        'A': [204],
        'Z': [81],
        'N': [123],
        'OneNeutronSeparationEnergy': [6656.08],
        'OneNeutronSeparationEnergyError': [0.29],
        'OneProtonSeparationEnergy': [6365.85],
        'OneProtonSeparationEnergyError': [1.25],
        'QFourBeta': [-12470.71],
        'QFourBetaError': [22.32],
        'QDeuteronAlpha': [13709.99],
        'QDeuteronAlphaError': [1.06],
        'QProtonAlpha': [8180.45],
        'QProtonAlphaError': [1.07],
        'QNeutronAlpha': [7700.97],
        'QNeutronAlphaError': [3.31],
    })

    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)

    line = io.StringIO(" 204 Tl  81    6656.0787    0.2907   6365.8379    1.2542 -12470.8182   22.6974  13710.0469    1.0612   8180.5147    1.0721   7701.0380    3.3084")
    parser = AMEReactionParserTwo(line, 2020)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
        'Symbol': ['Tl'],
        'A': [204],
        'Z': [81],
        'N': [123],
        'OneNeutronSeparationEnergy': [6656.0787],
        'OneNeutronSeparationEnergyError': [0.2907],
        'OneProtonSeparationEnergy': [6365.8379],
        'OneProtonSeparationEnergyError': [1.2542],
        'QFourBeta': [-12470.8182],
        'QFourBetaError': [22.6974],
        'QDeuteronAlpha': [13710.0469],
        'QDeuteronAlphaError': [1.0612],
        'QProtonAlpha': [8180.5147],
        'QProtonAlphaError': [1.0721],
        'QNeutronAlpha': [7701.0380],
        'QNeutronAlphaError': [3.3084],
    })

    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)
