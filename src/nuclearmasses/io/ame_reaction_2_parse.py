"""
The ame_reaction_2_parse module defines the ``AMEReactionTwoParser`` class. This class contains the logic required to
sort and organise the inputs to :meth:`pandas.read_fwf` dependent on the year of the file. Once parsed, known typos and
inconsistencies are cleaned from the resultant dataframe.
"""

import pandas as pd

from nuclearmasses.io.ame_reaction_2_file import AMEReactionTwoFile, AMEReactionTwoLayout
from nuclearmasses.utils.dataframe_utils import add_common_columns, read_fwf, strip_char_from_string_columns
from nuclearmasses.utils.type_defs import DataInput


class AMEReactionTwoParser:
    """
    Parse the second AME reaction file, doing the necessary preparation and clean-ups of data.

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
    layout : AMEReactionTwoLayout
        A storage class containing details of parameters and their locations in the line.
    column_limits : list[tuple[int|None, int|None]]
        The start and end positions of all parameters.
    """

    def __init__(self, filename: DataInput, year: int):
        self.filename: DataInput = filename
        self.year: int = year

        self.layout: AMEReactionTwoLayout = AMEReactionTwoFile(year).layout
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
            "A": "Int64",
            "Z": "Int64",
            "N": "Int64",
            "OneNeutronSeparationEnergy": "Float64",
            "OneNeutronSeparationEnergyError": "Float64",
            "OneProtonSeparationEnergy": "Float64",
            "OneProtonSeparationEnergyError": "Float64",
            "QFourBeta": "Float64",
            "QFourBetaError": "Float64",
            "QDeuteronAlpha": "Float64",
            "QDeuteronAlphaError": "Float64",
            "QProtonAlpha": "Float64",
            "QProtonAlphaError": "Float64",
            "QNeutronAlpha": "Float64",
            "QNeutronAlphaError": "Float64",
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
        return {
            "A": [""],
            "OneNeutronSeparationEnergy": ["", "*"],
            "OneNeutronSeparationEnergyError": ["", "*"],
            "OneProtonSeparationEnergy": ["", "*"],
            "OneProtonSeparationEnergyError": ["", "*"],
            "QFourBeta": ["", "*"],
            "QFourBetaError": ["", "*"],
            "QDeuteronAlpha": ["", "*"],
            "QDeuteronAlphaError": ["", "*"],
            "QProtonAlpha": ["", "*"],
            "QProtonAlphaError": ["", "*"],
            "QNeutronAlpha": ["", "*"],
            "QNeutronAlphaError": ["", "*"],
        }

    @staticmethod
    def _patch_1983(raw_df: pd.DataFrame) -> pd.DataFrame:
        """
        Modify the data from 1983 to make consistent

        Column header and units are repeated
        The A value is only present for the first isotope with the value

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
        raw_df = raw_df[(raw_df["A"] != "A") & (raw_df["Z"] != "")]

        # The A value is not in the column if it doesn't change so we need to fill down
        raw_df["A"] = raw_df["A"].ffill()

        return raw_df

    @staticmethod
    def _patch_2020(raw_df: pd.DataFrame) -> pd.DataFrame:
        """
        Modify the data from 2020 to make consistent

        Column header and units are repeated

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
        raw_df = raw_df[(raw_df["A"] != "A") & (raw_df["Z"] != "")]

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
        patch_registry = {
            1983: self._patch_1983,
            2020: self._patch_2020,
        }

        if self.year in patch_registry:
            raw_df = patch_registry[self.year](raw_df)

        return raw_df

    def read_file(self) -> pd.DataFrame:
        """
        Read the file-like object ``self.filename`` into a dataframe

        The ``AMEReactionTwoFile`` and other functions in this class have hopefully sanitized the column names, data
        types and locations of the date so we can now make the generic call to parse the file.

        Returns
        -------
        pandas.DataFrame
            A dataframe containing the parsed and organised contents of the second AME reaction data file
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
        # We use the NUBASE data to define whether or not an isotope is experimentally measured,
        # so for this data we'll just drop any and all '#' characters
        df = strip_char_from_string_columns(df, "#")

        df = self._apply_yearly_patch(df)

        df = add_common_columns(df, the_year=self.year)

        return df.astype(self._data_types())
