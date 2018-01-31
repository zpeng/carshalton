import pandas as pd
from simona.simona import Simona
from oracle.oracle import Oracle
from hugo.hugo import Hugo
from portfolio.portfolio import Portfolio

import time

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

simona = Simona(portfolio)
oracle = Oracle(portfolio)
hugo = Hugo(portfolio)

while True :
	simona.update()
	time.sleep(1)


