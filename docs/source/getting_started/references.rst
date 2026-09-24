References
==========

The values used to create the nuclear data table presented by this module are taken from the various published files from `AME`_ and `NUBASE`_.

The format of the files has changed over the years and is not always consistent within a single year so please ensure to always check the output.
No guarantee is supplied with regards to the accuracy of the data presented.
Estimated values are included, please always refer to the original sources.
All data should, however, be accurate.

The data files released by the papers linked below are used to create the mass tables output by this code.

There was no AME data published in 1997, but the 1995 AME matches the 1997 NUBASE according to section 4, "The tables" on P31 of `these proceedings <https://www.google.co.uk/books/edition/Atomic_Physics_at_Accelerators_Mass_Spec/3AbsCAAAQBAJ?hl=en>`_.
As a result the 1997 NUBASE data is referred to as being from 1995 for simplicity when merging data.

There are published papers for `1971`_ and `1977`_, but I can't find the associated data files.
If you are reading this and have a copy, know of someone with a copy, or have any information, please let me know via this issue `#13`_

- `AME1983 <https://doi.org/10.1016/0375-9474(85)90283-0>`_
- `AME1993 <https://doi.org/10.1016/0375-9474(93)90024-R>`_
- `AME1995 <https://doi.org/10.1016/0375-9474(95)00445-9>`_ + `NUBASE1997 <https://doi.org/10.1016/S0375-9474(97)00482-X>`_
- `AME2003 <https://doi.org/10.1016/j.nuclphysa.2003.11.002>`_ + `NUBASE2003 <https://doi.org/10.1016/j.nuclphysa.2003.11.001>`_
- `AME2012 <https://doi.org/10.1088/1674-1137/36/12/002>`_ + `NUBASE2012 <https://doi.org/10.1088/1674-1137/36/12/001>`_
- `AME2016 <https://doi.org/10.1088/1674-1137/41/3/030002>`_ + `NUBASE2016 <https://doi.org/10.1088/1674-1137/41/3/030001>`_
- `AME2020 <https://doi.org/10.1088/1674-1137/abddaf>`_ + `NUBASE2020 <https://doi.org/10.1088/1674-1137/abddae>`_

All data from the single NUBASE data file, the AME mass file and two reaction files are parsed and saved into the table.
Details from the different sources are merged on ``A``, ``Z`` and published year for each isotope, but otherwise, no comparison or validation is done on common values.


.. _AME: https://www-nds.iaea.org/amdc/
.. _NUBASE: https://www.anl.gov/phy/atomic-mass-data-resources
.. _1971: https://doi.org/10.1007/978-1-4684-7876-1_30
.. _1977: https://doi.org/10.1016/0092-640X(77)90004-3 
.. _#13: https://github.com/php1ic/nuclearmasses/issues/13

