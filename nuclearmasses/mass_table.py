import importlib.resources
import logging
import pathlib

import pandas as pd

from nuclearmasses.ame_mass_parse import AMEMassParser
from nuclearmasses.ame_reaction_1_parse import AMEReactionParserOne
from nuclearmasses.ame_reaction_2_parse import AMEReactionParserTwo
from nuclearmasses.nubase_parse import NUBASEParser


class MassTable:
    """Class for all of the mass data.

    Internally there are separate dataframes for the NUBASE and AME data as well as a combined one for all data
    """

    def __init__(self):
        """Do all of the work at construction."""
        self.data_path = importlib.resources.files("nuclearmasses.data")
        # print(self.data_path)
        self.nubase_years = [1995, 2003, 2012, 2016, 2020]
        self.nubase = pd.concat([self._parse_nubase_data(y) for y in self.nubase_years], ignore_index=True)
        self.ame_years = [1983, 1993, 1995, 2003, 2012, 2016, 2020]
        self.ame = pd.concat([self._parse_ame_data(y) for y in self.ame_years], ignore_index=True)
        self.full_data = self._combine_all_data()
        self._do_indexing()

    def _get_nubase_datafile(self, year: int) -> pathlib.Path:
        """Use the given year to locate the NUBASE mass table file and return the absolute path."""
        nubase_mass = self.data_path / pathlib.Path(str(year))
        nubase_mass = nubase_mass.resolve()

        match year:
            case 1995:
                nubase_mass = nubase_mass / "nubtab97.asc"
            case 2003:
                nubase_mass = nubase_mass / "nubtab03.asc"
            case 2012:
                nubase_mass = nubase_mass / "nubtab12.asc"
            case 2016:
                nubase_mass = nubase_mass / "nubase2016.txt"
            case 2020:
                nubase_mass = nubase_mass / "nubase_1.mas20"

        return nubase_mass

    def _get_ame_datafiles(self, year: int) -> tuple[pathlib.Path, pathlib.Path, pathlib.Path]:
        """Use the given year to locate the 3 AME data file and return the absolute paths."""
        data_dir = self.data_path / pathlib.Path(str(year))
        data_dir = data_dir.resolve()

        match year:
            case 1983:
                ame_mass = data_dir / "mass.mas83"
                ame_reaction_1 = data_dir / "rct1.mas83"
                ame_reaction_2 = data_dir / "rct2.mas83"
            case 1993:
                ame_mass = data_dir / "mass_exp.mas93"
                ame_reaction_1 = data_dir / "rct1_exp.mas93"
                ame_reaction_2 = data_dir / "rct2_exp.mas93"
            case 1995:
                ame_mass = data_dir / "mass_exp.mas95"
                ame_reaction_1 = data_dir / "rct1_exp.mas95"
                ame_reaction_2 = data_dir / "rct2_exp.mas95"
            case 2003:
                ame_mass = data_dir / "mass.mas03"
                ame_reaction_1 = data_dir / "rct1.mas03"
                ame_reaction_2 = data_dir / "rct2.mas03"
            case 2012:
                ame_mass = data_dir / "mass.mas12"
                ame_reaction_1 = data_dir / "rct1.mas12"
                ame_reaction_2 = data_dir / "rct2.mas12"
            case 2016:
                ame_mass = data_dir / "mass16.txt"
                ame_reaction_1 = data_dir / "rct1-16.txt"
                ame_reaction_2 = data_dir / "rct2-16.txt"
            case 2020:
                ame_mass = data_dir / "mass.mas20"
                ame_reaction_1 = data_dir / "rct1.mas20"
                ame_reaction_2 = data_dir / "rct2.mas20"

        return ame_mass, ame_reaction_1, ame_reaction_2

    def _parse_nubase_data(self, year: int) -> pd.DataFrame:
        """Get the NUBASE for the given year as a pandas.DataFrame."""
        return NUBASEParser(self._get_nubase_datafile(year), year).read_file()

    def _parse_ame_data(self, year: int) -> pd.DataFrame:
        """Combine all the AME files from the given year into a pandas.DataFrame."""
        ame_mass, ame_reaction_1, ame_reaction_2 = self._get_ame_datafiles(year)

        ame_mass_df = AMEMassParser(ame_mass, year).read_file()

        # Merge all 3 of the AME files/data frames into one
        common_columns = ['A', 'Z', 'N', 'TableYear', 'Symbol']
        temp_df = ame_mass_df.merge(AMEReactionParserOne(ame_reaction_1, year).read_file(), on=common_columns)
        return temp_df.merge(AMEReactionParserTwo(ame_reaction_2, year).read_file(), on=common_columns)

    def _combine_all_data(self) -> pd.DataFrame:
        """Combine all NUBASE and AME data into a single pandas DataFrame."""
        common_columns = ['A', 'Z', 'N', 'TableYear', 'Symbol']
        df = pd.merge(self.ame, self.nubase, on=common_columns, how='outer')

        df["NUBASERelativeError"] = abs(
            df["NUBASEMassExcessError"] / df["NUBASEMassExcess"]
        )
        df["AMERelativeError"] = abs(df["AMEMassExcessError"] / df["AMEMassExcess"])

        # 12C has a 0.0 +/ 0.0 mass excess by definition so calculating relative error -> NaN
        # Set the value to 0.0 as that's what it is
        df.loc[(df.Symbol == "C") & (df.A == 12), "NUBASERelativeError"] = 0.0
        df.loc[(df.Symbol == "C") & (df.A == 12), "AMERelativeError"] = 0.0

        # 198Au has a typo in it's decay mode in the 2012 table. It is recorded as '-'
        df.loc[(df.A == 198) & (df.Z == 79) & (df.TableYear == 2012), 'Decay'] = "B-"

        return df

    def _do_indexing(self) -> None:
        """
        Set the index of the dataframe to the table year. This is done in place so nothing is returned.

        param: Nothing

        :return: Nothing
        """
        self.nubase.set_index("TableYear", inplace=True)
        self.ame.set_index("TableYear", inplace=True)
        self.full_data.set_index("TableYear", inplace=True)
