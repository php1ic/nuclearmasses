nuclearmasses
=============

The package ``nuclearmasses`` provides convenient Python access to nuclear data published by the Atomic Mass Evaluation (`AME <https://www-nds.iaea.org/amdc/>`_) and `NUBASE <http://amdc.in2p3.fr/web/nubase_en.html>`_.
These datasets are published in different, specialised, formats, so ``nuclearmasses`` does the hard work of parsing and combining the data into a `pandas DateFrame <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_, making it simple to query and compare nuclear properties across different evaluations.

Full details and links to which tables are used and the papers they were released with can be found in the :doc:`References <getting_started/references>` page

No guarantee is supplied with regards to the accuracy of the data presented.
Estimated values are included, please always refer to the original sources.
All data should, however, be accurate.

.. toctree::
  :maxdepth: 3

  getting_started/index
  api

