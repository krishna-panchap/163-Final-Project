"""
Krishna Panchapagesan, Mark Pock
CSE 163 Final Project

Provides support for constructing an object representing the variation in
the global economy over a single war. Includes support for pandas .apply style
functionality through module-level methods.
"""


from numpy.polynomial.polynomial import Polynomial as poly
from sklearn.metrics import r2_score
import pandas as pd
import numpy as np


class War:
    """
    Represents the variation in the global economy (as determined by our global
    economic health index adjusted for inflation) over the course of a single
    war through polynomial regressions calibrated to the prewar, wartime, and
    postwar eras.
    """
    def __init__(self, war: str, final: pd.DataFrame, degree: int):
        """
        Given a str war and a DataFrame final in the format of datetime entries
        as an index and individual wars as columns, constructs a new War with
        polynomial regressions of the given degree for prewar, wartime, and
        postwar global economies.
        """
        self._war = war

        times = final[war]
        times.index = final.index

        pre = times[times == 1].index
        pre_avg = final.loc[pre, 'Adjusted Average'].dropna()
        pre_x = np.arange(0, len(pre_avg), 1)

        dur = times[times == 2].index
        dur_avg = final.loc[dur, 'Adjusted Average'].dropna()
        dur_x = np.arange(0, len(dur_avg), 1)

        post = times[times == 3].index
        post_avg = final.loc[post, 'Adjusted Average'].dropna()
        post_x = np.arange(0, len(post_avg), 1)

        self._pre: poly = poly.fit(pre_x, pre_avg, degree)
        self._dur: poly = poly.fit(dur_x, dur_avg, degree)
        self._post: poly = poly.fit(post_x, post_avg, degree)

        self._pre_r2 = r2_score(pre_avg, self._pre(pre_x))
        self._dur_r2 = r2_score(dur_avg, self._dur(dur_x))
        self._post_r2 = r2_score(post_avg, self._post(post_x))

    def pre(self) -> poly:
        """
        Returns a numpy.polynomial.polynomial.Polynomial regression for the
        prewar global economic health index.
        """
        return self._pre

    def dur(self) -> poly:
        """
        Returns a numpy.polynomial.polynomial.Polynomial regression for the
        wartime global economic health index.
        """
        return self._dur

    def post(self) -> poly:
        """
        Returns a numpy.polynomial.polynomial.Polynomial regression for the
        postwar global economic health index.
        """
        return self._post

    def __str__(self) -> str:
        """
        Returns a string representation of the War object using the
        coefficients of its polynomial regression.
        """
        return (self._war + ':\n' + str(self.pre().coef) + '\n' +
                str(self.dur().coef) + '\n' + str(self.post().coef))

    def r2(self) -> str:
        """
        Returns a string representation of the r-squared values associated with
        each polynomial regression.
        """
        return 'Pre: ' + str(self._pre_r2) + ', Dur: ' + str(self._dur_r2) \
            + ',Post: ' + str(self._post_r2)


def construct(war: str, final: pd.DataFrame, degree: int):
    """
    Provides support for a pandas-Series-style apply by constructing a single
    War with the given information (returning said war) and passing when that
    information is not complete (or relevant enough, e.g. case of single-year
    wars) in the DataFrame.
    """
    try:
        return War(war, final, degree)
    except ValueError:
        pass
