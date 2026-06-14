Usage
=====

Some examples of using the module

.. toctree::
   :maxdepth: 2

   plotting
   user_data


Quick Example
-------------

Get up and running by parsing all files into a single dataframe with:

.. code-block:: python

   from nuclearmasses.mass_table import MassTable

   table = MassTable().data

Once parsed, you have access to the pandas `dataframe`_ ecosystem to slice, sort or otherwise interrogate the data as required.

.. _dataframe: https://pandas.pydata.org/docs/reference/frame.html

For example, how has the mass excess of 14C changed over time according to NUBASE?

.. code-block:: python

   C_14 = table[(table['A'] == 14) & (table['Symbol'] == 'C')][['TableYear', 'NUBASEMassExcess', 'NUBASEMassExcessError']]
   print(C_14)

Any and all missing values are represented by pandas `NA`_ type for consistency.

.. _NA: https://pandas.pydata.org/docs/reference/api/pandas.NA.html#

.. code-block::

        TableYear  NUBASEMassExcess  NUBASEMassExcessError
   387       1983              <NA>                   <NA>
   388       1993              <NA>                   <NA>
   389       1995          3019.892                  0.004
   390       2003          3019.893                  0.004
   391       2012          3019.893                  0.004
   392       2016          3019.893                  0.004
   393       2020          3019.893                  0.004

As discussed in other sections, there was no published NUBASE table before 1997 so no data is provided for those years.
