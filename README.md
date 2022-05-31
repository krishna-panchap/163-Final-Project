# 163-Final-Project
## description 
The core of this project is centered on analyzing the effects of war on various
socio-economic scales.

We divide the scripts used to run the project roughly into three groups - 
cleaning data, analysing the data, and visualising the data. In addition, the utils
file contains utilities such as easy time series transformations used throughout
the scripts.

To clean (and in many respects obtain) the data, run the scripts as follows:
1. scrape_war_wiki constructs a list of wars dataset from Wikipedia pages which
   contain information about various wars.
2. cpi_cleanup performs a brief cleanup on the CPI dataset (Consumer Price Index)
   which, if not in the repo at time of use, should be downloaded from the
   official government website.
3. stocks_join aggregates the data from the DOW, Euronext 100, NASDAQ, NIKKEI 225,
   NYSE Composite, S&P 500, Shenzhen Component Index, and Shanghai Stock Exchange,
   data from which is stored in the repo currently. If not in the repo at time of
   use, use web_tables to (or manually) download from Yahoo Finance.
4. process_gdps takes gdp information from MacroTrends (and another site,
   TheBalance, which has GDP information for the US before 1960 (the MacroTrends
   start date)) to aggregate into a single gdp csv which has the gdps in billions.
5. stocks_averages uses the cleaned CPI data and the processed GDP data to
   generate an index for global economic health by weighting the major indices
   according to market capitalisation and GDP of region.
6. stocks_labelling transforms the index from 5, labelling each year with whether
   or not they are within certain wars using the dataset from scrape_war_wiki.