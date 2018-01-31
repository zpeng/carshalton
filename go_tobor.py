import pandas as pd
from portfolio.portfolio import Portfolio
from tobor.tobor import Tobor
from oracle.oracle import Oracle
from hugo.hugo import Hugo
import time
from datetime import datetime

p_config = {
	'name': 'LSE Testing',
  'watchList': ['HSBA','IMB','LLOY'],
	'cash': 500000,
	'fee': 995,
	'tax': 0.005,
	'sizePerInvestment' : 100000,
	'maxProportionPerHolding' : 0.3,
}
portfolio = Portfolio(p_config)

ds_config = {
	'data_source' : {
		'IMB': 'IMB_900_6M.csv',
		'LLOY': 'LLOY_900_6M.csv',
		'HSBA': 'HSBA_900_6M.csv',
	}
}
tobor = Tobor(ds_config, portfolio)

oracle = Oracle(portfolio)

hugo = Hugo(portfolio)

for x in range(0, 4300):
	print("Reading data at index: " + str(x))
	tobor.update()


portfolio.showStats()
portfolio.evaluation()