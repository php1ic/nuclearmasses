from nuclearmasses.ame_mass_parse import AMEMassParser

import io
import pandas as pd
import pandas.testing as pdt


def test_read_line():
    line = io.StringIO("  15   41   26   67 Fe    x  -45708.416       3.819      8449.9359     0.0570  B-   9613.3678     7.4900   66 950930.000       4.100")
    parser = AMEMassParser(line, 2020)
    parser.HEADER = 0
    parser.FOOTER = 0
    df = parser.read_file()

    expected = pd.DataFrame({
        'Symbol': ['Fe'],
        'A': [67],
        'Z': [26],
        'N': [41],
        'AMEMassExcess': [-45708.416],
        'AMEMassExcessError': [3.819],
        'BindingEnergyPerA': [8449.9359],
        'BindingEnergyPerAError': [0.0570],
        'BetaDecayEnergy': [9613.3678],
        'BetaDecayEnergyError': [7.4900],
        'AtomicMass': [66.950930],
        'AtomicMassError': [4.100/1.0e6],
    })
    expected = expected.astype(parser._data_types())

    pdt.assert_frame_equal(df, expected, check_like=True)

    # parser = AMEMassParser(pathlib.Path("."), 2012)
    # line = "  15   41   26   67 Fe    x  -46068.530    217.972     8455.310    3.253 B-   9253.245  218.067  66 950543.395    234.002"
    # d = parser._read_line(line)
    #
    # assert d['A'] == 67
    # assert d['Z'] == 26
    # assert d['N'] == 41
    # assert d['AMEMassExcess'] == -46068.530
    # assert d['AMEMassExcessError'] == 217.972
    # assert d['BindingEnergyPerA'] == 8455.310
    # assert d['BindingEnergyPerAError'] == 3.253
    # assert d['BetaDecayEnergy'] == 9253.245
    # assert d['BetaDecayEnergyError'] == 218.067
    # assert d['AtomicMass'] == 950543.395
    # assert d['AtomicMassError'] == 234.002
    #
    # parser = AMEMassParser(pathlib.Path("."), 2016)
    # line = "  15   41   26   67 Fe    x  -45610.155    270.285     8448.469    4.034 B-   9711.620  270.362  66 951035.482    290.163"
    # d = parser._read_line(line)
    #
    # assert d['A'] == 67
    # assert d['Z'] == 26
    # assert d['N'] == 41
    # assert d['AMEMassExcess'] == -45610.155
    # assert d['AMEMassExcessError'] == 270.285
    # assert d['BindingEnergyPerA'] == 8448.469
    # assert d['BindingEnergyPerAError'] == 4.034
    # assert d['BetaDecayEnergy'] == 9711.620
    # assert d['BetaDecayEnergyError'] == 270.362
    # assert d['AtomicMass'] == 951035.482
    # assert d['AtomicMassError'] == 290.163
    #
    # parser = AMEMassParser(pathlib.Path("."), 2020)
    # line = "  15   41   26   67 Fe    x  -45708.416       3.819      8449.9359     0.0570  B-   9613.3678     7.4900   66 950930.000       4.100"
    # d = parser._read_line(line)
    #
    # assert d['A'] == 67
    # assert d['Z'] == 26
    # assert d['N'] == 41
    # assert d['AMEMassExcess'] == -45708.416
    # assert d['AMEMassExcessError'] == 3.819
    # assert d['BindingEnergyPerA'] == 8449.9359
    # assert d['BindingEnergyPerAError'] == 0.0570
    # assert d['BetaDecayEnergy'] == 9613.3678
    # assert d['BetaDecayEnergyError'] == 7.4900
    # assert d['AtomicMass'] == 950930.00
    # assert d['AtomicMassError'] == 4.100
