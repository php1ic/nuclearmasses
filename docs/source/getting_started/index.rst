Getting Started
===============

.. toctree::
   :maxdepth: 3

   installation
   references
   usage/index


Quickstart
----------

To get up and running, install via pip

.. code-block:: bash

  pip install nuclearmasses

then access the table via

.. code-block:: python

  >>> from nuclearmasses.mass_table import MassTable
  >>> df = MassTable().data
  >>> print(df)

You now have access to the `pandas`_ ecosystem to sort, slice and analyse the data.
There is functionality external to pandas, and if you are interested in that see the :ref:`usage` section.

.. _pandas: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html
