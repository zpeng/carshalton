import requests
import pandas as pd
from datetime import datetime

class GoogleFinance:

  def __init__(self, config):
    self.url = 'https://finance.google.com/finance/getprices'
    self.config = {}
    self.config['i'] = config['i']
    self.config['x'] = config['x']
    self.config['p'] = config['p']

  def getPriceData(self, ticker):
    query = self.config
    query['q'] = ticker
    r = requests.get(self.url, params=query)
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


