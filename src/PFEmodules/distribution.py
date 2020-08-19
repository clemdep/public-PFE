import matplotlib.pyplot as plt
import pandas as pd
import re
import math


class Distribution(object):
    """
    Class to study the distribution of courses on several years.
    Needs to be instantiated with a dataframe.
    """

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def df_maker(self, year):
        """
        Prepares the dataframe for usage by other methods.
        Input: year: integer between 1998 and 2020.
        """
        return (self.dataframe[self.dataframe["EXERCICE"] == year].groupby("CODE_COURS")[
                "CODELEV"].nunique().reset_index(name="Nb students").sort_values(by="Nb students"))

    def color_maker(self, frame, sort_criterion):
        """
        Returns an array of color to maintain consistency of colors among the
        graphs of the class.
        Input:
          frame: pandas.Dataframe
          sort_criterion: string, must be the name of the frame column we wish
          to base the generated color array on.
        """
        colors = []
        color_DR = "#63386b"
        color_GG = "#66b84c"
        color_GC = "#6a46c3"
        color_EC = "#bfa04c"
        color_ML = "#cb54c3"
        color_RH = "#506833"
        color_MT = "#d06182"
        color_DS = "#5cad9b"
        color_PG = "#d85a36"
        color_GF = "#7d8bc5"
        color_MK = "#884835"

        for subject in frame.sort_values(by=str(sort_criterion))[
                "CODE_COURS"].iteritems():
            if subject[1] == "MK":
                colors.append(color_MK)
            elif subject[1] == "GF":
                colors.append(color_GF)
            elif subject[1] == "PG":
                colors.append(color_PG)
            elif subject[1] == "DS":
                colors.append(color_DS)
            elif subject[1] == "MT":
                colors.append(color_MT)
            elif subject[1] == "RH":
                colors.append(color_RH)
            elif subject[1] == "ML":
                colors.append(color_ML)
            elif subject[1] == "EC":
                colors.append(color_EC)
            elif subject[1] == "GC":
                colors.append(color_GC)
            elif subject[1] == "GG":
                colors.append(color_GG)
            elif subject[1] == "DR":
                colors.append(color_DR)
            else:
                raise ValueError("Something went wrong")
        return colors

    def single_plotter(self, year):
        """
        Plots the bar graph of the distribution of courses among types for a
        single year.
        Input: year: integer between 1998 and 2020.
        """
        ax = self.df_maker(year).plot(
            x="CODE_COURS", kind="bar", color=self.color_maker(
                self.df_maker, "Nb élèves"))
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x()
                                              * 1.005, p.get_height() * 1.02))

    def series_plotter(self, years, save=False, **kwargs):
        """
        Plots the bar graphs of the distribution of courses among types for
        several years and shows them side-by-side.
        WARNING : colors are hard-coded, DO NOT pass colors as kwargs !!!
        Input:
          years: list of integers between 1998 and 2020.
          save: bool, decides whether to save the figure or not, optional.
        """
        def define_length(n):
            """
            Internal method to calculate optimal number of subplots.
            Input: n: integer
            """
            x = (1 + math.sqrt(1 + 4 * n)) / 2
            return x
        # Initialize 2 counters used later
        i = 0
        j = 25
        # Decide which size of figure to use depending on number of years to
        # plot
        if len(years) in range(1, 5):
            fig, axes = plt.subplots(
                figsize=(
                    8, 8), nrows=int(
                    define_length(
                        len(years))), ncols=int(
                    define_length(
                        len(years))))
        elif len(years) in range(5, 10):
            fig, axes = plt.subplots(
                figsize=(
                    16, 16), nrows=int(
                    define_length(
                        len(years))), ncols=int(
                    define_length(
                        len(years))))
        else:
            fig, axes = plt.subplots(
                figsize=(
                    30, 30), nrows=int(
                    define_length(
                        len(years))), ncols=int(
                    define_length(
                        len(years))))

        # Initialize lists for loops below
        list_of_frames = []
        list_of_crs_total = []
        list_of_std_total = []
        # Make a dataframes list
        for year in years:
            list_of_frames.append(self.df_maker(year))
            list_of_crs_total.append(self.df_maker(year)["Nb students"].sum())
            list_of_std_total.append(
                self.dataframe[self.dataframe["EXERCICE"] == year]["CODELEV"].unique().shape[0])

        # Build an array of colors for each dataframe
        list_of_col_arrays = []
        for frame in list_of_frames:
            list_of_col_arrays.append(self.color_maker(frame, "Nb students"))
        # Plot the histograms
        for axe in axes.flatten():
            try:
                total_std = list_of_std_total[i]
                total_crs = list_of_crs_total[i]
                axe.title.set_text(
                    f"{years[i]} ({total_std} students, {total_crs} courses)")
                list_of_frames[i].plot(
                    x="CODE_COURS",
                    y="Nb students",
                    kind="bar",
                    ax=axe,
                    color=list_of_col_arrays[i],
                    **kwargs)
                axe.set_xlabel("Course category")
                for p in axe.patches:
                    axe.annotate(str(p.get_height()), (p.get_x()
                                                       * 1.005, p.get_height() * 1.02))
            except BaseException:
                # Remove unused graphs, if any
                while j > len(years):
                    axes.flat[j - 1].set_visible(False)
                    j = j - 1
                    if save:
                        plt.savefig("../graphs/distribution.png")
                pass
            i = i + 1
