"""
Krishna Panchapagesan, Mark Pock
CSE 163 Final Project

Takes a weighted average of data organised by year by the GDP of the region
encompassed in the data over time. In this case the data is data from four
of the largest and oldest stock indices - the S&P 500, the EUR 100, the
NIKKEI 225, and the SSE Component.
"""

import pandas as pd
from utils import time_series


def prev_year(date_int: int, gdps: pd.DataFrame, region: tuple) -> float:
    """
    Checks the previous year for its GDP if the current year does not have a
    GDP, returning the GDP of whichever is applicable in billions as a float.
    Note for behaviour - will recurse infinitely if no previous year exists.
    Data should be cleaned beforehand to mitigate the possibility.
    """
    try:
        return float(gdps.loc[str(date_int), region[1]])
    except KeyError:
        return prev_year(date_int - 1)


def nonzeros(index: int, filled: pd.DataFrame) -> int:
    """
    Gets the number of nonzero points in a single row given by an int index,
    returning the number as an int.
    """
    vals = filled.loc[index]
    return len(vals[vals != 0])


def main():
    ratios = time_series('ratios_benchmark', 'stocks/processed/', concat=False)
    gdps = time_series('pared', 'gdps/', concat=False).fillna(0)

    ratios = ratios.loc['1929':, (ratios.columns != 'DOW')
                        & (ratios.columns != 'NASDAQ')
                        & (ratios.columns != 'NYSE')
                        & (ratios.columns != 'SHZ')]
    regions = [('S&P', 'USA'), ('EUR', 'Europe'),
               ('NIKKEI', 'Japan'), ('SSE', 'China')]
    gdps['Total'] = sum([gdps[region] for region in gdps.columns])

    filled: pd.DataFrame = ratios.fillna(0)
    nums = pd.Series(filled.index).apply(lambda i: nonzeros(i, filled))

    ratios['Average'] = (filled['S&P'] * 0).fillna(0)

    for region in regions:
        adjusted = (filled[region[0]] * 0).fillna(0)
        for date in filled.iterrows():
            date = date[0]
            curr_gdp = prev_year(int(str(date).split('-')[0]))
            adjusted[date] = curr_gdp * filled.loc[date, region[0]]
        ratios[region[0] + ' Adjusted'] = adjusted

    ratios['Average'] = sum([ratios[region[0] + ' Adjusted']
                             for region in regions]) / nums
    ratios.to_csv('./datasets/stocks/processed/averaged.csv')


if __name__ == '__main__':
    main()
