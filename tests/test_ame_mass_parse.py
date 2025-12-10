from nuclearmasses.ame_mass_parse import AMEMassParser

import io
import pandas as pd
import pandas.testing as pdt


def test_1983_mass():
    # 67Fe was randomly selected to test the AME mass parsing. According to AME it didn't exist in 1983 so will use 67Ni
    line = io.StringIO(
        "0 11   39   28   67 Ni +n2p  -63742.471   19.056 582618.683   19.066    B-   3560.871   20.646   66 931570.167   20.457  -.0"
    )
    parser = AMEMassParser(line, 1983)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame(
        {
            "TableYear": [1983],
            "Symbol": ["Ni"],
            "A": [67],
            "Z": [28],
            "N": [39],
            "AMEMassExcess": [-63742.471],
            "AMEMassExcessError": [19.056],
            "BindingEnergyPerA": [582618.683 / 67],
            "BindingEnergyPerAError": [19.066 / 67],
            "BetaDecayEnergy": [3560.871],
            "BetaDecayEnergyError": [20.646],
            "AtomicMass": [66.931579167],
            "AtomicMassError": [20.457 / 1.0e6],
        }
    )
    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)


def test_1993_mass():
    line = io.StringIO(
        "0 15   41   26   67 Fe    x  -46574.693  465.747 567012.139  465.747    B-   8746.727  543.150   66 950000.000  500.000"
    )
    parser = AMEMassParser(line, 1993)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame(
        {
            "TableYear": [1993],
            "Symbol": ["Fe"],
            "A": [67],
            "Z": [26],
            "N": [41],
            "AMEMassExcess": [-46574.693],
            "AMEMassExcessError": [465.747],
            "BindingEnergyPerA": [567012.133 / 67],
            "BindingEnergyPerAError": [465.747 / 67],
            "BetaDecayEnergy": [8746.727],
            "BetaDecayEnergyError": [543.150],
            "AtomicMass": [66.950000000],
            "AtomicMassError": [500.0 / 1.0e6],
        }
    )
    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)


def test_1995_mass():
    # Yes the 1995 line is identical to the 1993 line
    line = io.StringIO(
        "  15   41   26   67 Fe    x  -46574.693  465.747 567012.133  465.747    B-   8746.727  543.150   66 950000.000  500.000"
    )
    parser = AMEMassParser(line, 1995)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame(
        {
            "TableYear": [1995],
            "Symbol": ["Fe"],
            "A": [67],
            "Z": [26],
            "N": [41],
            "AMEMassExcess": [-46574.693],
            "AMEMassExcessError": [465.747],
            "BindingEnergyPerA": [567012.133 / 67],
            "BindingEnergyPerAError": [465.747 / 67],
            "BetaDecayEnergy": [8746.727],
            "BetaDecayEnergyError": [543.150],
            "AtomicMass": [66.950000000],
            "AtomicMassError": [500.0 / 1.0e6],
        }
    )
    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)


def test_2003_mass():
    line = io.StringIO(
        "  15   41   26   67 Fe    x  -45692.348    415.570     8449.695    6.203 B-   9368.702  523.438  66 950947.244    446.132"
    )
    parser = AMEMassParser(line, 2003)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame(
        {
            "TableYear": [2003],
            "Symbol": ["Fe"],
            "A": [67],
            "Z": [26],
            "N": [41],
            "AMEMassExcess": [-45692.348],
            "AMEMassExcessError": [415.570],
            "BindingEnergyPerA": [8449.695],
            "BindingEnergyPerAError": [6.203],
            "BetaDecayEnergy": [9368.702],
            "BetaDecayEnergyError": [523.438],
            "AtomicMass": [66.950947244],
            "AtomicMassError": [446.132 / 1.0e6],
        }
    )
    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)


def test_2012_mass():
    line = io.StringIO(
        "  15   41   26   67 Fe    x  -46068.530    217.972     8455.310    3.253 B-   9253.245  218.067  66 950543.395    234.002"
    )
    parser = AMEMassParser(line, 2012)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame(
        {
            "TableYear": [2012],
            "Symbol": ["Fe"],
            "A": [67],
            "Z": [26],
            "N": [41],
            "AMEMassExcess": [-46068.530],
            "AMEMassExcessError": [217.972],
            "BindingEnergyPerA": [8455.310],
            "BindingEnergyPerAError": [3.253],
            "BetaDecayEnergy": [9253.245],
            "BetaDecayEnergyError": [218.067],
            "AtomicMass": [66.950543395],
            "AtomicMassError": [234.002 / 1.0e6],
        }
    )
    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)


def test_2016_mass():
    line = io.StringIO(
        "  15   41   26   67 Fe    x  -45610.155    270.285     8448.469    4.034 B-   9711.620  270.362  66 951035.482    290.163"
    )
    parser = AMEMassParser(line, 2016)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame(
        {
            "TableYear": [2016],
            "Symbol": ["Fe"],
            "A": [67],
            "Z": [26],
            "N": [41],
            "AMEMassExcess": [-45610.155],
            "AMEMassExcessError": [270.285],
            "BindingEnergyPerA": [8448.469],
            "BindingEnergyPerAError": [4.034],
            "BetaDecayEnergy": [9711.620],
            "BetaDecayEnergyError": [270.362],
            "AtomicMass": [66.951035482],
            "AtomicMassError": [290.163 / 1.0e6],
        }
    )
    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)


def test_2020_mass():
    line = io.StringIO(
        "  15   41   26   67 Fe    x  -45708.416       3.819      8449.9359     0.0570  B-   9613.3678     7.4900   66 950930.000       4.100"
    )
    parser = AMEMassParser(line, 2020)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame(
        {
            "TableYear": [2020],
            "Symbol": ["Fe"],
            "A": [67],
            "Z": [26],
            "N": [41],
            "AMEMassExcess": [-45708.416],
            "AMEMassExcessError": [3.819],
            "BindingEnergyPerA": [8449.9359],
            "BindingEnergyPerAError": [0.0570],
            "BetaDecayEnergy": [9613.3678],
            "BetaDecayEnergyError": [7.4900],
            "AtomicMass": [66.950930],
            "AtomicMassError": [4.100 / 1.0e6],
        }
    )
    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)
