"""
Krishna Panchapagesan, Mark Pock
CSE 163 Final Project

Insert documentation here.
"""

# used for type annotation
import pandas as pd
from typing import Iterable
from utils import time_series


def main():
    ratios = time_series('ratios_benchmark', 'stocks/processed/', concat=False)
    gdps = time_series('pared', 'gdps/', concat=False).fillna(0)

    ratios: pd.DataFrame = ratios.loc[:, (ratios.columns != 'DOW')
                                      & (ratios.columns != 'NASDAQ')
                                      & (ratios.columns != 'NYSE')
                                      & (ratios.columns != 'SHZ')]
    ratios = ratios.loc['1929':]
    regions = [('S&P', 'USA'), ('EUR', 'Europe'),
               ('NIKKEI', 'Japan'), ('SSE', 'China')]
    gdps['Total'] = sum([gdps[region] for region in gdps.columns])

    filled = ratios.fillna(0)
    nums = []
    for row in filled.iterrows():
        vals = row[1]
        nums.append(len(vals[vals != 0]))

    ratios['Average'] = (filled['S&P'] * 0).fillna(0)

    for region in regions:
        adjusted = (filled[region[0]] * 0).fillna(0)
        for date in filled.iterrows():
            date = date[0]

            def prev_year(date_int: int) -> float:
                """
                Checks the previous year for its GDP if the current year does
                not have a GDP, returning the GDP in billions as a float.
                """
                try:
                    return float(gdps.loc[str(date_int), region[1]])
                except KeyError:
                    return prev_year(date_int - 1)

            curr_gdp = prev_year(int(str(date).split('-')[0]))
            adjusted[date] = curr_gdp * filled.loc[date, region[0]]
        ratios[region[0] + ' Adjusted'] = adjusted

    ratios['Average'] = sum([ratios[region[0] + ' Adjusted']
                             for region in regions]) / nums
    ratios.to_csv('./datasets/stocks/processed/averaged.csv')


if __name__ == '__main__':
    main()
