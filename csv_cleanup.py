"""
Krishna Panchapagesan, Mark Pock
CSE 163 Final Project

This module cleans up the individual datasets to prepare for further analysis.
"""

import pandas as pd


def cleanup_cpi(cpi_file):
    cpi = pd.read_csv(cpi_file)
    cpi = cpi.loc[:, ((cpi.columns != 'HALF1') & (cpi.columns != 'HALF2'))]
    cpi.to_csv(cpi_file)


def main():
    cleanup_cpi('datasets/cpi.csv')


if __name__ == '__main__':
    main()
