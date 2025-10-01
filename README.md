# Nuclear Masses

[![Unit Tests](https://github.com/php1ic/nuclearmasses/actions/workflows/tests.yml/badge.svg)](https://github.com/php1ic/nuclearmasses/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/php1ic/nuclearmasses/graph/badge.svg?token=RNEI9PI6X8)](https://codecov.io/gh/php1ic/nuclearmasses)

## Introduction

Python package to parse the various files published by the [AME](https://www-nds.iaea.org/amdc/) and [NUBASE](http://amdc.in2p3.fr/web/nubase_en.html).
The files produced by the AME and NUBASE have unique formats so this package does the hard work for you and parses the data into a [pandas dataframe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) for simple access.

No guarantee is supplied with regards to the accuracy of the data presented.
Estimated values are included, please always refer to the original sources.
All data should, however, be accurate.

## Mass tables

The data files released by the papers linked below are used to create the mass tables read by this code.
There was no AME data published in 1997, but the 1995 AME matches the 1997 NUBASE according to section 4, "The tables" on P31 of [these proceedings](https://www.google.co.uk/books/edition/Atomic_Physics_at_Accelerators_Mass_Spec/3AbsCAAAQBAJ?hl=en).
As a result the 1997 NUBASE data is referred to as being from 1995 for simplicity when merging data.
- [AME1983](https://doi.org/10.1016/0375-9474(85)90283-0)
- [AME1993](https://doi.org/10.1016/0375-9474(93)90024-R)
- [AME1995](https://doi.org/10.1016/0375-9474(95)00445-9) + [NUBASE1997](https://doi.org/10.1016/S0375-9474(97)00482-X)
- [AME2003](https://doi.org/10.1016/j.nuclphysa.2003.11.002) + [NUBASE2003](https://doi.org/10.1016/j.nuclphysa.2003.11.001)
- [AME2012](https://doi.org/10.1088/1674-1137/36/12/002) + [NUBASE2012](https://doi.org/10.1088/1674-1137/36/12/001)
- [AME2016](https://doi.org/10.1088/1674-1137/41/3/030002) + [NUBASE2016](https://doi.org/10.1088/1674-1137/41/3/030001)
- [AME2020](https://doi.org/10.1088/1674-1137/abddaf) + [NUBASE2020](https://doi.org/10.1088/1674-1137/abddae)

The NUBASE files are read for all of the data values, with the AME files being used to populate an additional mass excess data field.
No comparison or validation is done on common values.

## Setup

The package is available on the Python Package Index so can be installed via pip
```bash
pip install nuclearmasses
```

Or you can clone the latest version from github
```bash
git clone https://github.com/php1ic/nuclearmasses
```

## Usage

Once installed or cloned, the data is available as a single dataframe indexed on the mass table year
```python
>>> from nuclearmasses.mass_table import MassTable
>>> df = MassTable().full_data
```
You can then interrogate, or extract, what ever information you want.
For example, how has the mass excess and it's accuracy changed overtime for 190Re according to the AME
```python
>>> df[(df['A'] == 190) & (df['Symbol'] == 'Re')][['AMEMassExcess', 'AMEMassExcessError']]
           AMEMassExcess  AMEMassExcessError
TableYear
1983          -35536.605             200.029
1993          -35557.789             145.549
1995          -35568.032             212.151
2003          -35566.326             149.248
2012          -35634.992              70.542
2016          -35635.830              70.852
2020          -35583.015               4.870
```
Or how do the mass excess of gold vary across the isotropic chain according to NUBASE in the most recent table for both experimentally measured and theoretical values
```python
>>> df.query("TableYear == 2020 and Symbol == 'Au'")[['A', 'NUBASEMassExcess', 'NUBASEMassExcessError', 'Experimental']]
             A  NUBASEMassExcess  NUBASEMassExcessError  Experimental
TableYear
2020       168            2530.0                  400.0         False
2020       169           -1790.0                  300.0         False
2020       170           -3700.0                  200.0         False
2020       171           -7562.0                   21.0          True
2020       172           -9320.0                   60.0          True
2020       173          -12832.0                   23.0          True
2020       174          -14060.0                  100.0         False
2020       175          -17400.0                   40.0          True
2020       176          -18520.0                   30.0          True
2020       177          -21546.0                   10.0          True
2020       178          -22303.0                   10.0          True
2020       179          -24989.0                   12.0          True
2020       180          -25626.0                    5.0          True
2020       181          -27871.0                   20.0          True
2020       182          -28304.0                   19.0          True
2020       183          -30191.0                    9.0          True
2020       184          -30319.0                   22.0          True
2020       185          -31858.1                    2.6          True
2020       186          -31715.0                   21.0          True
2020       187          -33029.0                   22.0          True
2020       188          -32371.3                    2.7          True
2020       189          -33582.0                   20.0          True
2020       190          -32834.0                    3.0          True
2020       191          -33798.0                    5.0          True
2020       192          -32772.0                   16.0          True
2020       193          -33405.0                    9.0          True
2020       194          -32211.9                    2.1          True
2020       195          -32567.1                    1.1          True
2020       196          -31138.7                    3.0          True
2020       197          -31139.8                    0.5          True
2020       198          -29580.8                    0.5          True
2020       199          -29093.8                    0.5          True
2020       200          -27240.0                   27.0          True
2020       201          -26401.0                    3.0          True
2020       202          -24353.0                   23.0          True
2020       203          -23143.0                    3.0          True
2020       204          -20390.0                  200.0         False
2020       205          -18570.0                  200.0         False
2020       206          -14190.0                  300.0         False
2020       207          -10640.0                  300.0         False
2020       208           -5910.0                  300.0         False
2020       209           -2230.0                  400.0         False
2020       210            2680.0                  400.0         False
```

## Contributing

If you have ideas for additional functionality or find bugs please create an [issue](https://github.com/php1ic/nuclearmasses/issues) or better yet a [pull request](https://github.com/php1ic/nuclearmasses/pulls).

## Known issues
- The half life from the NUBASE data is stored as the individual elements, a column with the value in seconds would be useful
```python
>>> df[(df['A'] == 14) & (df['Symbol'] == 'C')][['HalfLifeValue', 'HalfLifeUnit', 'HalfLifeError']]
           HalfLifeValue HalfLifeUnit  HalfLifeError
TableYear
1983                 NaN         <NA>            NaN
1993                 NaN         <NA>            NaN
1995                5.73           ky           0.04
2003                5.70           ky           0.03
2012                5.70           ky           0.03
2016                5.70           ky           0.03
2020                5.70           ky           0.03
```
- The decay mode field from the NUBASE data is stored 'as-is' from the file.
It looks like it can be split on the ';' character for isotopes where there is more than one mode.
A dictionary of {decay mode: fraction} may be the best way to store all of this information.
- Information from anything other than the ground state of an isotope is ignored when parsing the NUABSE file.
The selection of what is and what is not included appears random to me which is why I simply ignored for the moment.
