import pandas as pd


def time_series(filename: str, lib: str = '',
                concat: bool = False) -> pd.DataFrame:
    """
    Transforms a csv from the datasets folder into a Time Series as a pandas
    dataframe. The filename will be the name of the file alone without the
    csv extension, the library will be the internal folder (e.g. 'stocks/raw/')
    and concat represents whether or not to associate the names of the columns
    with the file.
    """
    path = './datasets/' + lib + filename + '.csv'
    df = pd.read_csv(path, index_col='Date', parse_dates=True)
    df = df.loc[:, df.columns != 'Unnamed: 0']
    if concat:
        df.columns = [(filename + ' ' + col) for col in df.columns]
    return df
