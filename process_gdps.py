"""
Krishna Panchapagesan, Mark Pock
CSE 163 Final Project

Modifies the CSV containing the ratios between stock index points and their
2010 prices to include a column for a weighted average based on GDP and
market capitalisation.
"""

import os
import pandas as pd
from utils import web_tables, time_series


def generate_csvs(regions: dict):
    """
    Given a dictionary regions containing the urls on MacroTrends for the
    gdps of certain regions as values for keys as the names of those regions,
    generates the csvs for them (and the csv for the US, whose data comes from
    a different site). Procedural, to be used only if csvs do not already
    exist or in the case of adding new regions from MacroTrends.
    """
    curr_csvs = os.listdir('./datasets/gdps/')
    if not all((item + '.csv') in curr_csvs for item in regions.keys()):
        for region in regions:
            web_tables(regions[region], region, 'gdps/', (1, 2))
    regions['USA'] = 'https://www.thebalance.com/us-gdp-by-year-3305543'
    if 'USA.csv' not in curr_csvs:
        web_tables(regions['USA'], 'USA', 'gdps/')


def tril_to_bil(trillion: str) -> float:
    """
    Given a str trillion representing the nominal GDP of the US in trillions of
    dollars as contained in the data from thebalance.com (in the form
    $num.num with occasional typing errors where the period is replaced by a
    comma), returns a float giving the billions of dollars corresponding to
    the amount.
    """
    return 1000 * float(trillion.split('$')[1].replace(',', '.'))


def clean_bil(billion: str) -> float:
    """
    Given a str billion representing the nominal GDP of a nation in billions of
    dollars as contained in the data from MacroTrends (in the form
    $num,num.numB, returns a float with the numerical amount isolated.
    """
    return float(billion[1:-1].replace(',', ''))


def main():
    macrotrends = 'https://www.macrotrends.net/countries/'
    gdp = 'gdp-gross-domestic-product'
    regions = {'Europe': macrotrends + 'EUU/european-union/' + gdp,
               'China': macrotrends + 'CHN/china/' + gdp,
               'Japan': macrotrends + 'JPN/japan/' + gdp}
    generate_csvs(regions)
    places = list(regions.keys())

    reg_dfs = [time_series(reg, 'gdps/', 'Year') for reg in regions]
    nomgdp = reg_dfs[-1]['USA Nominal GDP (trillions)']
    reg_dfs[-1].loc[:, 'USA GDP'] = nomgdp.apply(tril_to_bil)

    for i in range(len(reg_dfs) - 1):
        currgdp = reg_dfs[i].loc[:, places[i] + ' GDP']
        reg_dfs[i].loc[:, places[i] + ' GDP'] = currgdp.apply(clean_bil)

    gdp_series = [reg_dfs[i][places[i] + ' GDP'] for i in range(len(regions))]
    df = pd.DataFrame(gdp_series[0])
    for series in gdp_series[1:]:
        df = df.join(series, how='outer')
    df.columns = [col.split()[0] for col in df.columns]
    df.index.name = 'Date'
    df.to_csv('./datasets/gdps/pared.csv')


if __name__ == '__main__':
    main()
