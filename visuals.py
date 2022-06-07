'''
This module includes all the visualizations pertinent to the project
'''
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import time_series, inflation_adjust, clean_values


def wars_over_time(mega_dataset):
    '''
    plots the number of wars over time
    '''
    def count(i, mega_dataset):
        row = mega_dataset.loc[i, :]
        return len(row[row == 2])
    mega_dataset = mega_dataset.resample(rule='1Y').mean()
    num = pd.Series(mega_dataset.index).apply(lambda i: count(i, mega_dataset))
    num.index = mega_dataset.index
    num.name = 'War Count'
    num = pd.DataFrame(num)
    sns.lineplot(x=num.index, y='War Count', data=num)
    plt.xlabel('Time (Years)')
    plt.ylabel('Number of occuring wars')
    plt.title(('Number of Eventually-Terminated Wars' +
              ' Ongoing each Year Over Time'), y=1.08)
    plt.savefig('./visuals/wars_over_time.png', bbox_inches='tight')


def stock_vs_inflation_adjusted(stocks):
    '''
    plots our weighted average in comparison to the global market indices
    '''
    fig, ax = plt.subplots(1)
    stocks.sort_index(inplace=True)
    stocks = stocks.resample('1M').mean()
    inflation = time_series('inflation_ratios', col='Unnamed: 0', concat=False)
    vals = ['S&P Adjusted', 'EUR Adjusted', 'NIKKEI Adjusted',
            'SSE Adjusted', 'Average']
    for val in vals:
        adjusted = pd.Series(stocks.index).apply(lambda x: inflation_adjust(x,
                                                 val, stocks, inflation))
        adjusted.index = stocks.index
        stocks[val] = adjusted

    post_inflation = stocks[vals[0:-1]]
    post_inflation.plot(ax=ax, alpha=0.3)
    stocks.rename(columns={'Average': 'Weighted Average'}, inplace=True)
    average = stocks['Weighted Average']
    average.plot(ax=ax, legend=True, color='#000000')

    plt.title('Weighted Average of Inflation Adjusted Market Indices',
              y=1.08)
    plt.xlabel('Date (1929-2022)')
    plt.xticks(rotation=-45)
    plt.ylabel('Adjusted Market Value of each Index (in Millions)')
    plt.savefig('./visuals/average_index_post_inflation.png',
                bbox_inches='tight')
    return average


def economy_over_time(global_economy):
    '''
    plots the global economy over time
    '''
    fig, ax = plt.subplots(1)
    global_economy.plot(ax=ax)
    plt.title('Global Economic as a Weighted Average of Market Indexes',
              y=1.08)
    plt.xlabel('Date (1929-2022)')
    plt.ylabel('Global Economic Health Index (Millions)')
    plt.savefig('./visuals/global_economy.png', bbox_inches='tight',
                pad_inches=0.3)


def freedom_over_time(freedom):
    '''
    plots the percentages of free, not free, and partially free
    countries over time.
    '''
    def clean_percents(data):
        data = str(data)
        data = data[0:-1]
        return float(data)
    freedom['Year(s) Under Review**'] = \
        freedom['Year(s) Under Review**'] \
        .apply(clean_values)
    relevant_indexes = [4, 6, 8]
    for value in relevant_indexes:
        freedom[freedom.columns[value]] = \
            freedom[freedom.columns[value]] \
            .apply(clean_percents)
    freedom = freedom.sort_values('Year(s) Under Review**')
    relavent = freedom[['Year(s) Under Review**', '% of F Countries',
                        '% of PF Countries', '% of NF Countries']]
    relavent = relavent.set_index('Year(s) Under Review**')
    relavent.plot()
    plt.title('World Freedom Percentages of Countries over Time')
    plt.xlabel('Year (1972 to 2021)')
    plt.ylabel('Percentage')
    plt.savefig('./visuals/global_freedom.png', bbox_inches='tight')


def main():
    mega_dataset = pd.read_csv('./datasets/final.csv', parse_dates=True,
                               index_col='Date')
    wars_over_time(mega_dataset)
    stocks = time_series('averaged', 'stocks/processed/', concat=False)
    global_economy = stock_vs_inflation_adjusted(stocks)
    economy_over_time(global_economy)
    freedom = pd.read_csv('./datasets/freedom_by_year.csv')
    freedom_over_time(freedom)


if __name__ == '__main__':
    main()
