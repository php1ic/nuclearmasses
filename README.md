# Nuclear Masses

[![PyPI](https://img.shields.io/pypi/v/nuclearmasses)](https://pypi.org/project/nuclearmasses/)
[![Python Version](https://img.shields.io/pypi/pyversions/nuclearmasses)](https://pypi.org/project/nuclearmasses/)

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

There are published papers for [1971](https://doi.org/10.1007/978-1-4684-7876-1_30) and [1977](https://doi.org/10.1016/0092-640X(77)90004-3), but I can't find the associated data files.
If you are reading this and know of someone with a copy, or have any information, please let me know via this issue [#13](https://github.com/php1ic/nuclearmasses/issues/13)

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

Or you can clone the latest version from github and install locally.
All work is done on a feature branch so cloning and using `main` should be the similar to using the latest installed version from pip.
There may be some additional functionality, but nothing should have been removed.
```bash
git clone https://github.com/php1ic/nuclearmasses
cd nuclearmasses
pip install -e .
```

## Usage

> [!IMPORTANT]
> While every effort is made to maintain a stable API, this module is relatively new so users should not be surprised if there are changes between versions.
> If a breaking change has been introduced, it will always be highlighted in the [CHANGELOG](CHANGELOG.md).

The combination of AME and NUBASE values from all years is available as a single dataframe
```python
>>> from nuclearmasses.mass_table import MassTable
>>> df = MassTable().data
```
You can then interrogate, or extract, whatever information you want.
For example, how has the mass excess and its accuracy changed overtime for 190Re according to the AME
```python
>>> df[(df['A'] == 190) & (df['Symbol'] == 'Re')][['TableYear', 'AMEMassExcess', 'AMEMassExcessError']]
       TableYear  AMEMassExcess  AMEMassExcessError
16054       1983     -35536.605             200.029
16055       1993     -35557.789             145.549
16056       1995     -35568.032             212.151
16057       2003     -35566.326             149.248
16058       2012     -35634.992              70.542
16059       2016     -35635.830              70.852
16060       2020     -35583.015               4.870
```
Or how does the mass excess of gold vary across the isotopic chain according to NUBASE in the most recent table for both experimentally measured and theoretical values
```python
>>> df.query("TableYear == 2020 and Symbol == 'Au'")[['A', 'NUBASEMassExcess', 'NUBASEMassExcessError', 'Experimental']]
         A  NUBASEMassExcess  NUBASEMassExcessError  Experimental
14084  168            2530.0                  400.0         False
14189  169           -1790.0                  300.0         False
14291  170           -3700.0                  200.0         False
14391  171           -7562.0                   21.0          True
14492  172           -9320.0                   60.0          True
14591  173          -12832.0                   23.0          True
14687  174          -14060.0                  100.0         False
14781  175          -17400.0                   40.0          True
14874  176          -18520.0                   30.0          True
14968  177          -21546.0                   10.0          True
15060  178          -22303.0                   10.0          True
15153  179          -24989.0                   12.0          True
15244  180          -25626.0                    5.0          True
15334  181          -27871.0                   20.0          True
15419  182          -28304.0                   19.0          True
15503  183          -30191.0                    9.0          True
15588  184          -30319.0                   22.0          True
15673  185          -31858.1                    2.6          True
15757  186          -31715.0                   21.0          True
15842  187          -33029.0                   22.0          True
15926  188          -32371.3                    2.7          True
16007  189          -33582.0                   20.0          True
16088  190          -32834.0                    3.0          True
16164  191          -33798.0                    5.0          True
16243  192          -32772.0                   16.0          True
16320  193          -33405.0                    9.0          True
16401  194          -32211.9                    2.1          True
16480  195          -32567.1                    1.1          True
16560  196          -31138.7                    3.0          True
16637  197          -31139.8                    0.5          True
16713  198          -29580.8                    0.5          True
16788  199          -29093.8                    0.5          True
16861  200          -27240.0                   27.0          True
16935  201          -26401.0                    3.0          True
17012  202          -24353.0                   23.0          True
17089  203          -23143.0                    3.0          True
17163  204          -20390.0                  200.0         False
17237  205          -18570.0                  200.0         False
17308  206          -14190.0                  300.0         False
17382  207          -10640.0                  300.0         False
17456  208           -5910.0                  300.0         False
17528  209           -2230.0                  400.0         False
17603  210            2680.0                  400.0         False
```

## Contributing

If you have ideas for additional functionality or find bugs please create an [issue](https://github.com/php1ic/nuclearmasses/issues) or better yet a [pull request](https://github.com/php1ic/nuclearmasses/pulls).

We use a combination of [ruff](https://docs.astral.sh/ruff/) and [mypy](https://www.mypy-lang.org/) to keep things tidy and hopefully catch errors and bugs before they happen.
The command below returns no errors or issues so should be run after any code changes.
We might add a CI pipeline in the future, but for the moment, it's a manual process.
```bash
ruff format && ruff check && mypy src
```

## Known issues

- [#6](https://github.com/php1ic/nuclearmasses/issues/6) The decay mode field from the NUBASE data is stored 'as-is' from the file.
It looks like it can be split on the ';' character for isotopes where there is more than one mode.
A dictionary of {decay mode: fraction} may be the best way to store all of this information.
- [#7](https://github.com/php1ic/nuclearmasses/issues/7) Information from anything other than the ground state of an isotope is ignored when parsing the NUBASE file.
The selection of what is and what is not included appears random to me which is why I simply ignored for the moment.
