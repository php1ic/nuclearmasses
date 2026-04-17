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
Or how does the mass excess of lithium vary across the isotopic chain according to NUBASE in the most recent table for both experimentally measured and theoretical values
```python
>>> df.query("TableYear == 2020 and Symbol == 'Li'")[['A', 'NUBASEMassExcess', 'NUBASEMassExcessError', 'Experimental']]
      A  NUBASEMassExcess  NUBASEMassExcessError  Experimental
38    3        28670.0000              2000.0000         False
59    4        25320.0000               210.0000          True
79    5        11680.0000                50.0000          True
104   6        14086.8804                 0.0014          True
133   7        14907.1050                 0.0040          True
161   8        20945.8000                 0.0500          True
196   9        24954.9100                 0.1900          True
229  10        33053.0000                13.0000          True
264  11        40728.3000                 0.6000          True
298  12        49010.0000                30.0000          True
336  13        56980.0000                70.0000          True
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
