import requests
from datetime import datetime
import pandas as pd


def get_price_data(query):
	r = requests.get("https://finance.google.com/finance/getprices", params=query)
	lines = r.text.splitlines()
	data = []
	basetime = 0
	for price in lines:
		cols = price.split(",")
		if cols[0][0] == 'a':
			basetime = int(cols[0][1:])
			data.append([datetime.fromtimestamp(basetime), float(cols[4]), float(cols[2]), float(cols[3]), float(cols[1]), int(cols[5])])
		elif cols[0][0].isdigit():
			date = basetime + (int(cols[0])*int(query['i']))
			data.append([datetime.fromtimestamp(date), float(cols[4]), float(cols[2]), float(cols[3]), float(cols[1]), int(cols[5])])
	return pd.DataFrame(data, columns = ['Timestamp','Open', 'High', 'Low', 'Close', 'Volume'])


for ticker in ['HSBA','LLOY','IMB','BATS','ASC','BOO','VOD','BKG','PSN','GSK','AZN','BTG','TSCO','BP']:
	interval = '300' # 1 Day
	period = '12M'

	param = {
		'q': ticker, # Stock symbol (ex: "AAPL")
		'i': interval, # Interval size in seconds ("86400" = 1 day intervals)
		'x': "LON", # Stock exchange symbol on which stock is traded (ex: "NASD")
		'p': period # Period (Ex: "1Y" = 1 year)
	}

	data = get_price_data(param)
	data.to_csv(ticker+'_'+interval+'_'+period+'.csv', encoding='utf-8')



