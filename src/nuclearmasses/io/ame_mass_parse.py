"""
The ame_mass_parse module defines the ``AMEMassParser`` class. This class contains the logic required to sort and
organise the inputs to :meth:`pandas.read_fwf` dependent on the year of the file. Once parsed, known typos and
inconsistencies are cleaned from the resultant dataframe.
"""

import pandas as pd

from nuclearmasses.io.ame_mass_file import AMEMassFile, AMEMassLayout
from nuclearmasses.utils.dataframe_utils import (
    add_common_columns,
    calculate_relative_error,
    read_fwf,
    strip_char_from_string_columns,
)
from nuclearmasses.utils.type_defs import DataInput


class AMEMassParser:
    """
    Parse the AME mass file, doing the necessary preparation and clean-ups of data.

    There are some quirks to the format used in the file. It's based on fixed-width format, but deviates in various
    places so additional work is required once the file is parsed.

    Parameters
    ----------
    filename : DataInput
        The file-like object to parse.
    year : int
        The published year of the data file.

    Attributes
    ----------
    filename : DataInput
        The file-like object to parse.
    year : int
        The published year of the data file.
    layout : AMEMassLayout
        A storage class containing details of parameters and their location in the line.
    column_limits : list[tuple[int|None, int|None]]
        The start and end positions of all parameters
    """

    def __init__(self, filename: DataInput, year: int):
        self.filename: DataInput = filename
        self.year: int = year

        self.layout: AMEMassLayout = AMEMassFile(year=year).layout
        self.column_limits: list[tuple[int | None, int | None]] = [
            (getattr(self.layout, start), getattr(self.layout, end)) for _, start, end in self.layout.positions
        ]

    def _column_names(self) -> list[str]:
        """
        Set the column name depending on the year.

        Returns
        -------
        list[str]
            An ordered list of the columns that exist in the file.
        """
        return self.layout.columns

    def _data_types(self) -> dict:
        """
        Set the column data types depending on the year.

        Returns
        -------
        dict[str, str]
            A dictionary of the columns that exist and their data type
        """
        return {
            "TableYear": "Int64",
            "Symbol": "string",
            "N": "Int64",
            "Z": "Int64",
            "A": "Int64",
            "AMEMassExcess": "Float64",
            "AMEMassExcessError": "Float64",
            "AMERelativeError": "Float64",
            "BindingEnergyPerA": "Float64",
            "BindingEnergyPerAError": "Float64",
            "BetaDecayEnergy": "Float64",
            "BetaDecayEnergyError": "Float64",
            "AtomicMass": "Float64",
            "AtomicMassError": "Float64",
            "DataSource": "Int64",
        }

    def _na_values(self) -> dict:
        """
        Set the columns that have empty fields so should be set to NaN during the initial parse.

        Returns
        -------
        dict[str, list[str]]
            A dictionary of the columns that will have values that should be interpreted as NaN.
        """
        na_vals = {
            "A": [""],
            "BetaDecayEnergy": ["", "*"],
            "BetaDecayEnergyError": ["", "*"],
        }

        if self.year != 1983:
            na_vals.pop("A")

        return na_vals

    def _correct_binding_energy(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert Binding Energy values into Binding Energy per A

        The data from 1995 and earlier records total Binding Energy. Post 1995 it was recorded as Binding Energy per A.
        With the assumption that any future data will also be per A, we label the column accordingly and use this
        function to correct the stored value.

        Parameters
        ----------
        raw_df : pd.DataFrame
            The raw dataframe, immediately after the file parse.

        Returns
        -------
        pd.DataFrame
            The updated dataframe with corrections made.
        """
        a = raw_df["A"].astype(float)

        raw_df["BindingEnergyPerA"] = raw_df["BindingEnergyPerA"].astype(float) / a
        raw_df["BindingEnergyPerAError"] = raw_df["BindingEnergyPerAError"].astype(float) / a

        return raw_df

    @staticmethod
    def _patch_1983(raw_df: pd.DataFrame) -> pd.DataFrame:
        """
        Modify the data from 1983 to make consistent

        Column header and units are repeated
        The A value is only present for the first isotope with the value
        Some isomeric states are present. We will ignore for the time being

        Parameters
        ----------
        raw_df : pd.DataFrame
            The raw dataframe, immediately after the file parse.

        Returns
        -------
        pd.DataFrame
            The updated dataframe with corrections made.
        """
        # The repeated header lines are parsed so we can use the values that are now in specific columns to drop rows
        raw_df = raw_df[
            (raw_df["A"] != "A") & (~raw_df["AMEMassExcess"].astype("string").str.contains("keV", na=False))
        ]

        # If the A value is missing, use the last valid value
        raw_df["A"] = raw_df["A"].ffill()

        # Assume any row with A and Z equal to the previous row represents an isomeric state and drop it
        raw_df = raw_df[~((raw_df["A"] == raw_df["A"].shift()) & (raw_df["Z"] == raw_df["Z"].shift()))]

        return raw_df

    def _apply_yearly_patch(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        """
        Correct known issues in the data, e.g. typos

        There are typos in specific fields for various years as well as some column misalignments.
        This function should be called immediately after the initial parse to apply the necessary corrections, allowing
        the proceeding functions to be generic and not need to test for formatting issues.

        Parameters
        ----------
        raw_df : pd.DataFrame
            The raw dataframe, immediately after the file parse.

        Returns
        -------
        pd.DataFrame
            The updated dataframe with corrections made.
        """
        if self.year == 1983:
            raw_df = self._patch_1983(raw_df)
            raw_df = self._correct_binding_energy(raw_df)
        elif self.year in (1993, 1995):
            raw_df = self._correct_binding_energy(raw_df)

        return raw_df

    def _reconstruct_atomic_mass(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        """
        Reconstruct the atomic mass from the components recorded in the data file

        The data file has the atomic mass as 2 columns, the atomic number as an integer and the part after the integer
        as a left zero padded float with its own decimal place e.g. "9 001234.567". We want it as a single value so a
        small amount of work needs to be done to correctly concatenate these two columns. The error value is given
        relative to the float so we also need to appropriately scale that number.

        Parameters
        ----------
        raw_df : pd.DataFrame
            The raw dataframe, immediately after the file parse.

        Returns
        -------
        pd.DataFrame
            The updated dataframe with corrections made.
        """
        # Combine the two columns to create the atomic mass then drop the redundant column
        raw_df["AtomicMass"] = (
            raw_df["AtomicNumber"].astype("string")
            + "."
            + raw_df["AtomicMass"].astype("string").str.replace(".", "", regex=False)
        )
        raw_df = raw_df.drop(columns=["AtomicNumber"])
        # We need to rescale the error value because we combined the two columns
        raw_df["AtomicMassError"] = raw_df["AtomicMassError"].astype(float) / 1.0e6

        return raw_df

    def read_file(self) -> pd.DataFrame:
        """
        Read the file-like object ``self.filename`` into a dataframe

        The ``AMEMassFile`` and other functions in this class have hopefully sanitised the column names, data types and
        locations of the date so we can now make the generic call to parse the file.

        Returns
        -------
        pandas.DataFrame
            A dataframe containing the parsed and organised contents of the AME mass data file
        """
        df = read_fwf(
            self.filename,
            colspecs=self.column_limits,
            names=self._column_names(),
            na_values=self._na_values(),
            keep_default_na=False,
            on_bad_lines="warn",
            skiprows=self.layout.HEADER,
            skipfooter=self.layout.FOOTER,
        )
        # We use the NUBASE data to define whether an isotope is experimentally measured,
        # so for this data we'll just drop any and all '#' characters
        df = strip_char_from_string_columns(df, "#")

        df = self._apply_yearly_patch(df)

        df = self._reconstruct_atomic_mass(df)

        df = calculate_relative_error(df, "AME")
        df = add_common_columns(df, the_year=self.year)

        return df.astype(self._data_types())
