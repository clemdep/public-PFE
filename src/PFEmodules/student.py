import matplotlib.pyplot as plt
import pandas as pd
import re
import math


class Student(object):
    """
    Class defining a student and implementing methods to study the evolution
    of their elective choices over time.
    Instantion requires:
      codelev: int, mandatory
      dfr: pandas.dataframe, optional. Default dataframe is the main df.

      WARNING: not specifying a dataframe on instantiation WILL make calling
      any kind of loop instantiating multiple students EXTREMELY SLOW.
    """

    def __init__(self, codelev, dfr=None):
        self.codelev = codelev
        # Below needs a fix
        self.dfr = dfr[dfr["CODELEV"] == codelev] if dfr is not None else pd.read_csv(
            "../data/df_redux.csv")
        self.list_of_years = self.dfr["CODE_ANNEE"].unique().tolist()

    def find_major(self, year=None):
        """
        Given a year, will output the major choice of a student on specified
        year. If no year is specified, the whole academic track is used.
        Input: year: str, optional.
        """
        if year:
            return self.dfr[self.dfr["CODE_ANNEE"] ==
                            year]["CODE_COURS"].value_counts().idxmax()
        else:
            return self.dfr["CODE_COURS"].value_counts().idxmax()

    def find_second_major(self):
        """
        Finds second most frequent course of a student and puts it in a list.
        Input: None.
        """
        try:
            ret = self.dfr["CODE_COURS"].value_counts().nlargest(2).index[1]
            return ret
        except:
            return None


    def count_courses_student(self, year=None):
        """
        Will return total number of courses taken by student
        If a year is provided, will count on the year. If not, will count on the entire academic track.
        Input: year: str, optional
        """
        if year:
            return self.dfr[self.dfr["CODE_ANNEE"] ==
                            year]["CODE_COURS"].unique().shape[0]
        else:
            return self.dfr.shape[0]

    def progress(self, verbose=False):
        """
        Returns a dict of the student majors over the years, if records permit.
        Otherwise i.e. if student has only 1 year of records, returns None.
        Input: verbose: bool, optional.
        """
        if len(self.list_of_years) < 2:
            if verbose:
                print(f"Student {self.codelev} doesn't have enough records.")
            return None
        else:
            dict_of_majors = {}
            for year in self.list_of_years:
                dict_of_majors[year] = self.find_major(year)
            return dict_of_majors

    def count_courses_over_years(self):
        """
        Returns a dictionary in the form {Academic Year: Nb of courses}
        counting the number of courses taken by the student in the given year
        """
        dict_of_cnt = {}
        for year in self.list_of_years:
            dict_of_cnt[year] = self.count_courses_student(year)
        return dict_of_cnt

    def show_courses_over_years(self):
        """
        Returns a dictionary in the form {Academic Year: [MK, DS...]} showing
        all the courses taken by the student on each of the years.
        """
        dict_of_courses = {}
        for year in self.list_of_years:
            dict_of_courses[year] = self.dfr[self.dfr["CODE_ANNEE"]
                                             == year]["CODE_COURS"].unique().tolist()
        return dict_of_courses
