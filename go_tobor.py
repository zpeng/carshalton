import pandas as pd
from portfolio.portfolio import Portfolio
from tobor.tobor import Tobor
from oracle.oracle import Oracle
from hugo.hugo import Hugo
import time
from datetime import datetime

p_config = {
	'name': 'LSE Testing',
  'watchList': ['HSBA','LLOY','IMB'],
	'cash': 6000 * 100,
	'fee': 995,
	'tax': 0.005,
	'sizePerInvestment' : 2000 * 100,
	'maxProportionPerHolding' : 0.3,
}
portfolio = Portfolio(p_config)

ds_config = {
	'data_source' : {
		'IMB': 'IMB_3600_13M.csv',
		'LLOY': 'LLOY_3600_13M.csv',
		'HSBA': 'HSBA_3600_13M.csv',
	}
}
tobor = Tobor(ds_config, portfolio)

oracle = Oracle(portfolio)

hugo = Hugo(portfolio)

for x in range(0, 2200):
	print("Reading data at index: " + str(x))
	tobor.update()


portfolio.showStats()
portfolio.evaluation()