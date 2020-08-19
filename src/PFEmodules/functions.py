"""
Defines some functions for use in the Jupyter Notebooks. Should be imported by
adding "../src" to sys.path and import functions.
"""
import matplotlib.pyplot as plt
import sys
sys.path.append("../src")
from PFEmodules import *
from collections import Counter
from collections import OrderedDict
import pandas as pd
import re
import math
import numpy as np
from IPython.display import display_html
from IPython.core.display import display, HTML


def get_promo(dataframe):
    """
    Returns 4-digit integer containing the promotion for each record
    Input: dataframe: pandas.DataFrame
    """
    return int(str(dataframe["CODELEV"])[0:4])


def assign_subject(dataframe):
    """
    Returns new column containing the course code
    Input: dataframe: pandas.Dataframe
    """
    if "GC" in dataframe["CODE_EPR"]:
        return "GC"
    elif "EI" in dataframe["CODE_EPR"]:
        return "EC"
    # Code all MK34x, MK35x and MK99x courses as Data Science
    elif re.match(r"^MK34.|^MK35.|MK99|MK991", dataframe["CODE_EPR"]):
        return "DS"
    # Code all relevant courses to Maker"s Lab courses
    elif re.match(r"^WA.|MAK.|WEB.", dataframe["CODE_EPR"]):
        return "ML"
    elif "MK" in dataframe["CODE_EPR"]:
        return "MK"
    elif "GF" in dataframe["CODE_EPR"]:
        return "GF"
    elif "RH" in dataframe["CODE_EPR"]:
        return "RH"
    elif "DR" in dataframe["CODE_EPR"]:
        return "DR"
    elif "PG" in dataframe["CODE_EPR"]:
        return "PG"
    elif "EC" in dataframe["CODE_EPR"]:
        return "EC"
    elif "GG" in dataframe["CODE_EPR"]:
        return "GG"
    elif "MT" in dataframe["CODE_EPR"]:
        return "MT"
    else:
        print(dataframe["CODE_EPR"])
        raise ValueError("Unhandled error in func assign_subject")


def assign_year(dataframe):
    """
    Assigns a coded year column for easier manipulation
    Input: dataframe: pandas.Dataframe
    """
    if int(dataframe["EXERCICE"]) - \
            int(str(dataframe["CODELEV"])[0:4]) < 2:
        return "2A"
    elif int(dataframe["EXERCICE"]) - int(str(dataframe["CODELEV"])[0:4]) == 2:
        return "3A"
    elif int(dataframe["EXERCICE"]) - int(str(dataframe["CODELEV"])[0:4]) == 3:
        return "4A"
    elif int(dataframe["EXERCICE"]) - int(str(dataframe["CODELEV"])[0:4]) >= 4:
        return "AS"
    else:
        raise ValueError("Error in assign_year func")

def course_taken_nb(course_code, dataframe):
    """
    Given a course code and a dataframe, will return number of times this
    course has been taken by student
    Input: course_code: integer
    """
    return dataframe[dataframe["CODE_EPR"] == course_code].shape[0]


def omnivorism_cat(row):
    """
    Assigns a category between 1 and 5 based on the level of omnivorism
    Input: row: pandas.Dataframe
    """
    if int(row["CTO"]) in range(1, 2):
        return 1
    elif int(row["CTO"]) in range(2, 4):
        return 2
    elif int(row["CTO"]) in range(4, 6):
        return 3
    elif int(row["CTO"]) in range(6, 8):
        return 4
    elif int(row["CTO"]) in range(8, 11):
        return 5
    else:
        raise ValueError


def display_side_by_side(dfs: list, captions: list):
    """
    credits : https://stackoverflow.com/a/57832026/11798696
    Display tables side by side to save vertical space
    Input:
        dfs: list of pandas.DataFrame
        captions: list of table captions
    """
    output = ""
    combined = dict(zip(captions, dfs))
    for caption, df in combined.items():
        output += df.style.set_table_attributes(
            "style='display:inline'").set_caption(caption)._repr_html_()
        output += "\xa0\xa0\xa0"
    display(HTML(output))


def omni_cat_avg(list_of_dictionaries, plottable=False):
    """
    Given a list of dictionaries {"academic year" : "nb of courses taken"}
    such as the one output by student.count_courses_over_years method will
    return a dict {"academic year": "average nb of courses taken"}.
    Input:
      list_of_dictionaries : list of dict
      plottable : if set to True, will return a dict {"academic year" : nb of
      courses taken} with nb of courses taken being an int instead of a list so
      that it can be plotted.
    """
    A2cnt = 0
    A2tot = 0
    A3cnt = 0
    A3tot = 0
    A4cnt = 0
    A4tot = 0
    AScnt = 0
    AStot = 0

    for dictionary in list_of_dictionaries:
        for key, value in dictionary.items():
            if key == "2A":
                A2tot = A2tot + int(dictionary[key])
                A2cnt += 1
            elif key == "3A":
                A3tot = A3tot + int(dictionary[key])
                A3cnt += 1
            elif key == "4A":
                A4tot = A4tot + int(dictionary[key])
                A4cnt += 1
            elif key == "AS":
                AStot = AStot + int(dictionary[key])
                AScnt += 1
            else:
                print("unhandled")
                return None

    if A2cnt == 0:
        A2ret = 0
    else:
        A2ret = A2tot / A2cnt
    if A3cnt == 0:
        A3ret = 0
    else:
        A3ret = A3tot / A3cnt
    if A4cnt == 0:
        A4ret = 0
    else:
        A4ret = A4tot / A4cnt
    if AScnt == 0:
        ASret = 0
    else:
        ASret = AStot / AScnt

    if plottable:
        ret_dict = {"2A": A2ret, "3A": A3ret, "4A": A4ret, "AS": ASret}
    else:
        ret_dict = {"2A": [A2ret], "3A": [A3ret], "4A": [A4ret], "AS": [ASret]}

    return ret_dict


def promo_slicer(dataframe, promo):
    """
    Given a dataframe containing a "PROMO" column, will slice the dataframe
    and retrieve only the records matching the promo input.
    Input:
      dataframe: pandas.DataFrame
      promo: int between 1998 and 2020.
    """
    return dataframe[dataframe["PROMO"] == promo]


def category_slicer(dataframe, category):
    """
    Given a dataframe containing a "CAT_OMNI" column, will the dataframe and
    return only the records matching the category input.
    Input:
      dataframe: pandas.DataFrame
      category: int between 1 and 5
    """
    return dataframe[dataframe["CAT_OMNI"] == category]


def multi_numeric_plotter(
        data,
        ax=None,
        colors=None,
        total_width=0.8,
        single_width=1,
        legend=True,
        figsize=(
            12,
            8),
        **kwargs):
    """
    Draws a bar plot with multiple bars per data point.
    Parameters
    ----------
    ax : matplotlib.pyplot.axis
    The axis we want to draw our plot on.

    data: dictionary
    A dictionary containing the data we want to plot. Keys are the names of the
    data, the items is a list of the values.

    Example:
    data = {
    "x":[1,2,3],
    "y":[1,2,3],
    "z":[1,2,3],
    }

    colors : array-like, optional
    A list of colors which are used for the bars. If None, the colors
    will be the standard matplotlib color cyle. (default: None)

    total_width : float, optional, default: 0.8
    The width of a bar group. 0.8 means that 80% of the x-axis is covered
    by bars and 20% will be spaces between the bars.

    single_width: float, optional, default: 1
    The relative width of a single bar within a group. 1 means the bars
    will touch eachother within a group, values less than 1 will make
    these bars thinner.

    legend: bool, optional, default: True
    If this is set to true, a legend will be added to the axis.
    """
    # This section is the actual plotting
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))
        retflag = True
    else:
        retflag = False
    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Iterate over all data
    for i, (name, values) in enumerate(data.items()):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2
        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset,
                         y,
                         width=bar_width * single_width,
                         align="center",
                         color=colors[i % len(colors)],
                         edgecolor="k",
                         )

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])
        ax.set_xlabel("Category")
        ax.set_ylabel("Nb of courses taken")

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys())
    
    if retflag:
        return ax

def single_plotter(data):
    """
    Plots a bar plot for a given dict
    Input: data: a dictionary
    """
    keys = data.keys()
    values = data.values()
    plt.bar(keys, values)


def dict_cleaner(dic):
    """
    Returns a purged dictionary without None values
    Input: dic: dict
    """
    return {k: v for k, v in dic.items() if v is not None}


def complementary_pie_chart(course,frame,ax=None, return_counter=False):
    """
    Plots a pie chart of the courses complementary to the major specified as 
    an argument. The resulting pie chart will show the distribution of the 
    courses selected by students who majored in "course"
    Input:
      course: integer. The major of which we want to plot the complementary 
      courses.
      frame: pandas.DataFrame. The dataframe to take the data from.
    """
    # Make a list of students with course as their major
    list_of_course_major = []
    student_count = 0
    for code in frame["CODELEV"].drop_duplicates():
        student = Student(code, frame)
        if student.find_major() == course:
            list_of_course_major.append(student.codelev)
            student_count += 1
        else:
            pass

    # Make a list of the second most-taken course for the students in the list_of_course_major
    list_of_complementary = []
    for code in list_of_course_major:
        student = Student(code, frame)
        list_of_complementary.append(student.find_second_major())
    list_of_complementary

    # Create a counter to compute the frequency
    counter = Counter(list_of_complementary)
    # Remove Nones from the counter
    del counter[None]

    # Plot a pie chart based on the data
    retflag = True
    if ax is None:
        fig, ax = plt.subplots(figsize=(8,8))
        retflag = False

    labels = []
    sizes = []
    for key, value in counter.items():
        labels.append(key)
        sizes.append(value)
    colors=color_maker(labels)
    ax.pie(sizes, labels=labels, autopct="%1.1f%%",
            shadow=True, colors=colors, startangle=90)
    ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_xlabel(f"Second major of students with major {course} ({student_count} students)")
    ax.legend()
    ax.set_facecolor("w")

    if retflag and return_counter:
        return ax, counter
    elif retflag:
        return ax


def color_maker(list_of_courses):
    """
    Returns an array of color to maintain consistency of colors among the
    graphs of the class.
    Input:
      frame: pandas.Dataframe
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

    for subject in list_of_courses:
        if subject == "MK":
            colors.append(color_MK)
        elif subject == "GF":
            colors.append(color_GF)
        elif subject == "PG":
            colors.append(color_PG)
        elif subject == "DS":
            colors.append(color_DS)
        elif subject == "MT":
            colors.append(color_MT)
        elif subject == "RH":
            colors.append(color_RH)
        elif subject == "ML":
            colors.append(color_ML)
        elif subject == "EC":
            colors.append(color_EC)
        elif subject == "GC":
            colors.append(color_GC)
        elif subject == "GG":
            colors.append(color_GG)
        elif subject == "DR":
            colors.append(color_DR)
        else:
            raise ValueError("Something went wrong")
    return colors
