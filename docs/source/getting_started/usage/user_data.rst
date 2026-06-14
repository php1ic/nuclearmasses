User Data
=========

Functionality exists for a user to add their own data into the combined table.
The function :py:meth:`add_user_data` is a method of the :py:class:`MassTable` class and takes data in `json`_ format and adds it to the table.

.. _json: https://www.json.org

An identifier column `DataSource` already exists and for all published data and is set to 0.
Along with providing the new data, a user can specify a value for `DataSource`, otherwise a value of 1 is automatically assigned.
The ability to specify a value means multiple data sources can be added whilst maintaining the ability to distinguish.
If no value is given, the value of 1 will always be used.

To ensure uniqueness, values for `A` and `Z` must be part of the data.
With the assumption that you would like to compare and contrast this new data with the published values, the name associated with your data must also match existing columns.
I know this doesn't quite make sense, as you might not necessarily want to assign your new mass to either AME or NUBASE, but in general, the columns are generic so I'm sure you'll work it out.

Let's imagine I have a new measurement for the mass excess of 100Ag at -78136.4 +/- 0.6 and I want to add it to the table

.. code-block:: python

   >>> # Addition is done on the class level so create an instance of the MassTable
   >>> from nuclearmasses.mass_table import MassTable
   >>> table = MassTable()
   >>> # This step doesn't need to be done, but, for demonstration purposes,
   >>> # extract the table data and check the current details for 100Ag
   >>> df = table.data
   >>> df.query("Symbol == 'Ag' and A == 100")[['A', 'Z', 'NUBASEMassExcess', 'NUBASEMassExcessError', 'DataSource']])
           A  NUBASEMassExcess  NUBASEMassExcessError  DataSource
   6976  100               NaN                    NaN           0
   6977  100               NaN                    NaN           0
   6978  100          -78180.0                   80.0           0
   6979  100          -78150.0                   80.0           0
   6980  100          -78138.0                    5.0           0
   6981  100          -78138.0                    5.0           0
   6982  100          -78138.0                    5.0           0
   >>> # Add our new value to the NUBASE columns
   >>> table.add_user_data('[{"A": 100, "Z": 47, "NUBASEMassExcess": -78136.4, "NUBASEMassExcessError": 0.6}]')
   >>> # The underlying table has been modified, so we need to get the latest version
   >>> df = table.data
   >>> # Re-run the query to see the new value, notice the value for DataSource has been set to 1
   >>> df.query("Symbol == 'Ag' and A == 100")[['A', 'Z', 'NUBASEMassExcess', 'NUBASEMassExcessError', 'DataSource']])
            A  NUBASEMassExcess  NUBASEMassExcessError  DataSource
   6976   100               NaN                    NaN           0
   6977   100               NaN                    NaN           0
   6978   100          -78180.0                   80.0           0
   6979   100          -78150.0                   80.0           0
   6980   100          -78138.0                    5.0           0
   6981   100          -78138.0                    5.0           0
   6982   100          -78138.0                    5.0           0
   21421  100          -78136.4                    0.6           1
   >>> # We can add the same data but this time assign to a different source
   >>> table.add_user_data('[{"A": 100, "Z": 47, "NUBASEMassExcess": -78136.4, "NUBASEMassExcessError": 0.6}]', source=5)
   >>> # Again, this modifies the underlying dataframe so we need to fetch the updated version
   >>> df = table.data
   >>> # Run the query and see that our new data is there twice against two different sources
   >>> df.query("Symbol == 'Ag' and A == 100")[['A', 'Z', 'NUBASEMassExcess', 'NUBASEMassExcessError', 'DataSource']])
            A  NUBASEMassExcess  NUBASEMassExcessError  DataSource
   6976   100               NaN                    NaN           0
   6977   100               NaN                    NaN           0
   6978   100          -78180.0                   80.0           0
   6979   100          -78150.0                   80.0           0
   6980   100          -78138.0                    5.0           0
   6981   100          -78138.0                    5.0           0
   6982   100          -78138.0                    5.0           0
   21421  100          -78136.4                    0.6           1
   21422  100          -78136.4                    0.6           5

Now let's imagine that we have a large new data set in a json file, but have forgotten to add the `Experimental` attribute and for reasons, it is not possible to edit or update the file with this additional information.
When reading in the file, we can pass a dictionary as a parameter, and the keys will be used as the column names, with the values used as value to for all new isotopes.

In the following example, we will assume the data is in a file `new_data.json` and of type `pathlib`_.

.. _pathlib: https://docs.python.org/3/library/pathlib.html

.. code-block:: python

   >>> import pathlib
   >>> from nuclearmasses.mass_table import MassTable
   >>> table = MassTable()
   >>> missed_values = {'Experimental': True}
   >>> new_data = pathlib.Path('new_data.json')
   >>> table.add_user_data(new_data, common_values=missed_values)
   >>> # All isotopes from new_data.json will have their Experimental column assigned to True

If an existing column is not populated with new data, it is assigned the value pd.NA.
We do not try and infer what a value could, should or might be.

