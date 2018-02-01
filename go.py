import pandas as pd
from portfolio.portfolio import Portfolio
from tobor.tobor import Tobor
from oracle.oracle import Oracle
from hugo.hugo import Hugo
import time
from datetime import datetime

p_config = {
	'name': 'LSE Testing',
	'watchList': ['HSBA','LLOY','IMB','BATS','ASC','BOO','VOD','BKG','PSN','GSK','AZN','BTG','TSCO','BP'],
	'cash': 10000 * 100,
	'fee': 995,
	'tax': 0.005,
	'sizePerInvestment' : 2000 * 100,
	'maxProportionPerHolding' : 0.2,
}
portfolio = Portfolio(p_config)

ds_config = {
	'mode': 'live', # mock vs live
	'live': { # Using Google Finance
	  'tickerList': p_config['watchList'],
		'gf_config': {
			'i': 900, # Interval size in seconds ("86400" = 1 day intervals)
			'x': "LON", # Stock exchange symbol on which stock is traded (ex: "NASD")
			'p': "6M", # Period (Ex: "1Y" = 1 year)
		},
	},
	'mock' : { # local CSV data
		'IMB': 'IMB_3600_13M.csv',
		'LLOY': 'LLOY_3600_13M.csv',
		'HSBA': 'HSBA_3600_13M.csv',
	},
	'startIndex': 10, # row index from the data source start with
}
tobor = Tobor(ds_config, portfolio)
oracle = Oracle(portfolio)
hugo = Hugo(portfolio)

for x in range(ds_config['startIndex'], 4300):
	print("Reading data point at index: " + str(x))
	tobor.update()


portfolio.showStats()
portfolio.evaluation()