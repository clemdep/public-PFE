
class DataframeCounter(object):
    """
    Class implements various counters for dataframe objects throughout the
    notebooks.
    Input: pandas.Dataframe
    """

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def courses_counter(self, code_cours):
        """
        Provided a list of tuples and a dataframe, will return how many times
        the courses of the tuples have been taken.
        Input: course code: integer
        """
        list_of_tuples = []
        for cours in code_cours:
            list_of_tuples.append(
                self.dataframe[self.dataframe["CODE_EPR"] == cours].shape)
        return sum(i for i, j in list_of_tuples)

    def get_course_from_code(self, course_code):
        """
        Provided a course code, will return the lib of this course
        Input: course code: integer
        """
        result_1 = self.dataframe[["CODE_EPR", "libepr"]].drop_duplicates(
            subset="CODE_EPR")[self.dataframe["CODE_EPR"] == course_code]["libepr"].to_string()
        result_2 = "".join([i for i in result_1 if not i.isdigit()])
        result = result_2.strip()
        return result
