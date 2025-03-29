# Nuclear Masses

## Introduction

Python package to parse the various files published by the [AME](https://www-nds.iaea.org/amdc/) and [NUBASE](http://amdc.in2p3.fr/web/nubase_en.html).
The files produced by the AME and NUBASE have unique formats so this package does the hard work for you and parses the data into a [pandas dataframe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) for simple access.

No guarantee is supplied with regards to the accuracy of the data presented.
Estimated values are included, please always refer to the original sources.
All data should, however, be accurate.

## Mass tables

The data files released by the papers linked below are used to create the mass tables read by this code
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

