Data Ingestion
==============


As much as possible the data is stored in its original form, and a new column created where necessary.
The main deviation from this is the `#` symbol, and its use as a theoretical or estimated value marker.
The Mass Excess value in the NUBASE data is used to signify if the isotope has been experimentally verified or any given year, and after the initial ingestion, a search is carried out and if a `#` is found the `Experimental` column set to `True`.
A global find and replace is then applied swapping `#` for a single space to maintain line locations.
For the AME data, the initial search is not carried and the global replace immediately carried out.

Below are details for any values that have more than trivial amounts of manipulation applied to the raw values.

AME
---

Binding Energy
^^^^^^^^^^^^^^

The data from 1983, 1993 and 1995 is for the Binding Energy, but all year since record Binding Energy **per nucleon**.
It was decided to use the current form of the data so the values from 1983, 1993 and 1995 are immediately converter to per nucleon.

Atomic Mass
^^^^^^^^^^^

The atomic mass is stored as two columns of the format "A bcdefg.xyz" with the single value being "A.bcdefgxyz" and the second column having units micro-u.
To we remove the '.' from the second string and concatenate the result with the first, using a '.' as the separator then cast as a float.
The error is recorded in a third column and is relative to the second string so we can simply divide that value by 1e6 to convert to the correct units.

NUBASE
------

Half-life
^^^^^^^^^

The half-life is stored as an human readable value, e.g. "1.5 min 0.3" or "5.70 ky 0.03" with the error being in the same units.
We maintain a dictionary to convert from these units, transforming both the value and error into new columns with units if seconds.
This functionality is available via scipy, but it was decided that adding scipy as a dependency for this fairly simple mapping was not worth it.

Decay Modes
^^^^^^^^^^^

The final field for each isotope contains details about how the isotope decays.
It is a ';' separated string with a variety of representations depending on the decay mode, the type of error (symmetric or asymmetric), value limits, isotopic ratios for stable isotopes and more.
Via a regex, we parse each component into a dataclass and the column becomes a list of these classes.

The original value from the file is stored in the `DecayModesRaw` column and each instance of the class contains the string used to create it. 
The :py:class:`DecayMeasurement` class has the following attributes and as we are passing in strings, we can make use of the `Decimal` type to hopefully help with comparisons. 

.. code-block :: python

  @dataclass(frozen=True, kw_only=True)
  class DecayMeasurement:
      """
      Storage class for decay mode details
      """

      decay_type: str
      operator: str | None
      percentage: Decimal | None
      error: Decimal | None = None
      upper_error: Decimal | None = None
      lower_error: Decimal | None = None
      annotation: str | None = None
      status: str = "reported"
      raw: str | None = None
  

