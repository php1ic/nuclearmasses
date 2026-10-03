# Nuclear Masses

[![PyPI](https://img.shields.io/pypi/v/nuclearmasses)](https://pypi.org/project/nuclearmasses/)
[![Python Version](https://img.shields.io/pypi/pyversions/nuclearmasses)](https://pypi.org/project/nuclearmasses/)

[![Unit Tests](https://github.com/php1ic/nuclearmasses/actions/workflows/tests.yml/badge.svg)](https://github.com/php1ic/nuclearmasses/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/php1ic/nuclearmasses/graph/badge.svg?token=RNEI9PI6X8)](https://codecov.io/gh/php1ic/nuclearmasses)
[![Read the Docs](https://img.shields.io/readthedocs/nuclearmasses)](https://nuclearmasses.readthedocs.io/)

[![DOI](https://zenodo.org/badge/953582888.svg)](https://doi.org/10.5281/zenodo.23124585)

## Introduction

The package `nuclearmasses` provides convenient Python access to nuclear data published by the Atomic Mass Evaluation ([AME](https://www-nds.iaea.org/amdc/)) and [NUBASE](http://amdc.in2p3.fr/web/nubase_en.html).
These datasets are published in different, specialised formats, so `nuclearmasses` does the hard work of parsing and combining the data into a [pandas DateFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html), making it simple to query and compare nuclear properties across different evaluations.

No guarantee is supplied with regards to the accuracy of the data presented.
Estimated values are included, please always refer to the original sources.
All data should, however, be accurate.

Documentation is here - https://nuclearmasses.readthedocs.io/

As a brief example, the combination of AME and NUBASE values from all years is available as a single DateFrame
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

## Mass tables

The data files released by the papers linked below are used to create the mass tables output by this code.
There was no AME data published in 1997, but the 1995 AME matches the 1997 NUBASE according to section 4, "The tables" on P31 of [these proceedings](https://www.google.co.uk/books/edition/Atomic_Physics_at_Accelerators_Mass_Spec/3AbsCAAAQBAJ?hl=en).
As a result the 1997 NUBASE data is referred to as being from 1995 for simplicity when merging data.

There are published papers for [1971](https://doi.org/10.1007/978-1-4684-7876-1_30) and [1977](https://doi.org/10.1016/0092-640X(77)90004-3), but I can't find the associated data files.
If you are reading this and have a copy, know of someone with a copy, or have any information, please let me know via this issue [#13](https://github.com/php1ic/nuclearmasses/issues/13)

- [AME1983](https://doi.org/10.1016/0375-9474(85)90283-0)
- [AME1993](https://doi.org/10.1016/0375-9474(93)90024-R)
- [AME1995](https://doi.org/10.1016/0375-9474(95)00445-9) + [NUBASE1997](https://doi.org/10.1016/S0375-9474(97)00482-X)
- [AME2003](https://doi.org/10.1016/j.nuclphysa.2003.11.002) + [NUBASE2003](https://doi.org/10.1016/j.nuclphysa.2003.11.001)
- [AME2012](https://doi.org/10.1088/1674-1137/36/12/002) + [NUBASE2012](https://doi.org/10.1088/1674-1137/36/12/001)
- [AME2016](https://doi.org/10.1088/1674-1137/41/3/030002) + [NUBASE2016](https://doi.org/10.1088/1674-1137/41/3/030001)
- [AME2020](https://doi.org/10.1088/1674-1137/abddaf) + [NUBASE2020](https://doi.org/10.1088/1674-1137/abddae)

All data from the single NUBASE data file, the AME mass file and two reaction files are parsed and saved into the table.
Details from the different sources are merged on `A`, `Z` and published year for each isotope, but otherwise, no comparison or validation is done on common values.


## Installation and Setup

The package is available on the [Python Package Index](https://pypi.org/project/nuclearmasses/) so can be installed via pip
```bash
pip install nuclearmasses
```
Or you can clone the latest version from github and install locally.
All work is done on a feature branch so cloning and using `main` should be the same as using the latest installed version from pip.
There may be some additional functionality, but nothing should have been removed.
```bash
git clone https://github.com/php1ic/nuclearmasses
cd nuclearmasses
pip install -e .
```

## Contributing

Details about contributing to the project are in [CONTRIBUTING](https://github.com/php1ic/nuclearmasses/blob/main/CONTRIBUTING.md)


## Known issues

- [#6](https://github.com/php1ic/nuclearmasses/issues/6) The decay mode field from the NUBASE data is stored 'as-is' from the file.
It looks like it can be split on the ';' character for isotopes where there is more than one mode.
A dictionary of {decay mode: fraction} may be the best way to store all of this information.
- [#7](https://github.com/php1ic/nuclearmasses/issues/7) Information from anything other than the ground state of an isotope is ignored when parsing the NUBASE file.
The selection of what is and what is not included appears random to me which is why I simply ignored for the moment.
