import matplotlib.pyplot as plt
import pandas as pd
import re
import math


class Frequency(object):
    """
    This class regroups useful methods for working on the frequency of courses
    between omnivorism categories.
    Input:
        dataframe: pandas.Dataframe
    """

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def frame_maker(self, dataframe, category):
        """
        Extracts a sub-dataframe containing only the records with CAT_OMNI
        equal to the category argument.
        Input:
          dataframe: pandas.DataFrame
          category: integer between 1 and 5
        """
        sub_dataframe = dataframe[dataframe["CAT_OMNI"] == category]
        return sub_dataframe

    def compute_frequency(self):
        """
        Returns the frequency of courses in a category.
        Returns a pandas.Series
        """
        return (self.frame_maker(self.dataframe)["CODE_COURS"].value_counts(
        ) / len(self.frame(maker(self.dataframe))))

    def plot_piecharts(
            self,
            cats=5,
            mode="multiple",
            category=None,
            color_list=None):
        """
        Plots one or several piecharts representing the distribution of courses
        taken by students belonging to one or several categories.
        Can work in two modes, default is multiple, can also work in single.
        Multiple mode plots categories 1 to cats argument.
        Single mode plots the distribution of category specified in the args.
        Input:
          Multiple mode:
            cats: integer between 1 and 5, optional, default plots all cats
            color_list: list of 11 colors in matplotlib format, optional
          Single mode:
            category: integer between 1 and 5
            color_list: same as above.
        """
        color_list = color_list or [
            "#00876c",
            "#4c9c85",
            "#78b19f",
            "#a0c6b9",
            "#c8dbd5",
            "#f1f1f1",
            "#f1cfce",
            "#eeadad",
            "#df676e",
            "#e76b77",
            "#de425b"]

        # Block for plotting several charts
        if mode == "multiple":
            # Building the subplot
            fig, axes = plt.subplots(3, 2, figsize=(30, 15))
            axe_tup = axes.flatten()
            for i in range(0, cats):
                # Building the arrays to plot
                x = self.frame_maker(
                    self.dataframe,
                    i + 1)["CODE_COURS"].value_counts().index.to_numpy()
                y = (self.frame_maker(self.dataframe, i + 1)
                     ["CODE_COURS"].value_counts()).to_numpy()
                percentage = 100. * y / y.sum()

                # Building the elements of the plot
                patches, texts = axe_tup[i].pie(
                    y, colors=color_list, startangle=90, radius=1.2)
                labels = ["{0} - {1:1.2f} %".format(i, j)
                          for i, j in zip(x, percentage)]

                sort_legend = True
                if sort_legend:
                    patches, labels, dummy = zip(*sorted(zip(patches, labels, y),
                                                         key=lambda x: x[2],
                                                         reverse=True))

                fig_chart = axe_tup[i].legend(patches, labels, loc="best",
                                              bbox_to_anchor=(-0.1, 1.), fontsize=8)
                axe_tup[i].set_title(
                    f"Distribution of courses taken by students of category {i+1}")
            i = 6
            while i > cats:
                # Removing the unused subplots
                axes.flat[i - 1].set_visible(False)
                i = i - 1

       # Block for single plotting
        else:

            x = self.frame_maker(self.dataframe, category)[
                "CODE_COURS"].value_counts().index.to_numpy()
            y = (self.frame_maker(self.dataframe, category)
                 ["CODE_COURS"].value_counts()).to_numpy()
            percentage = 100. * y / y.sum()

            # Create the figure
            fig, ax = plt.subplots()
            patches, texts = ax.pie(
                y, colors=color_list, startangle=90, radius=2)
            labels = ["{0} - {1:1.2f} %".format(i, j)
                      for i, j in zip(x, percentage)]

            # Create the legend
            patches, labels, dummy = zip(*sorted(zip(patches, labels, y),
                                                 key=lambda x: x[2],
                                                 reverse=True))

            fig_chart = ax.legend(patches, labels, loc="best",
                                  bbox_to_anchor=(-0.1, 1.), fontsize=8)
            ax.set_title(
                f"Répartition des cours pris par les étudiants de catégorie {category}",
                loc="right")
            plt.show()
            ax.set_facecolor("w")
