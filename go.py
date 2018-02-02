import pandas as pd
from dataSource.dataSource import DataSource
from portfolio.portfolio import Portfolio
from tobor.tobor import Tobor
from oracle.oracle import Oracle
from hugo.hugo import Hugo
import time
from datetime import datetime

p_config = {
	'name': 'LSE Testing',
	'watchList': ['HSBA','LLOY','BATS','ASC','BOO','VOD','BKG','PSN','GSK','AZN','BTG','TSCO','BP','AAL','BLT','RIO'],
	'cash': 10000 * 100,
	'fee': 995,
	'tax': 0.005,
	'sizePerInvestment' : 2000 * 100,
	'maxNumHoldingsPerStock' : 1,
}

ds_config = {
	'mode': 'live', # mock vs live
	'live': { # Using Google Finance
	  'tickerList': p_config['watchList'],
		'gf_config': {
			'i': 3600, # Interval size in seconds ("86400" = 1 day intervals)
			'x': "LON", # Stock exchange symbol on which stock is traded (ex: "NASD")
			'p': "12M", # Period (Ex: "1Y" = 1 year)
		},
	},
	'mock' : { # local CSV data
		'LLOY': 'LLOY_3600_13M.csv',
		'HSBA': 'HSBA_3600_13M.csv',
	},
}

dataSource = DataSource(ds_config) # dataSource has loaded up with data
portfolio = Portfolio(p_config, dataSource)

startIndex = 10
tobor = Tobor(dataSource, portfolio, startIndex)
oracle = Oracle(portfolio)
hugo = Hugo(portfolio)

for x in range(startIndex, 2020):
	print("Reading data point at index: " + str(x))
	tobor.update()

print("All data has been processed, just to evaluate and record the result...")
portfolio.evaluation()
print("All Done!")