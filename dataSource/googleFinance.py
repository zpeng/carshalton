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
    previous_value = 0.0
    for price in lines:
      cols = price.split(",")
      if cols[0][0] == 'a':
        basetime = int(cols[0][1:])
        data.append([datetime.fromtimestamp(basetime), float(cols[4]), float(cols[2]), float(cols[3]), float(cols[1]), int(cols[5])])
        previous_value = float(cols[1])
      elif cols[0][0].isdigit():
        date = basetime + (int(cols[0])*int(query['i']))
        close = self.__dataSanityCheck(previous_value, float(cols[1]), datetime.fromtimestamp(date), ticker)
        data.append([datetime.fromtimestamp(date), float(cols[4]), float(cols[2]), float(cols[3]), close, int(cols[5])])
        previous_value = float(cols[1])
    return pd.DataFrame(data, columns = ['Timestamp','Open', 'High', 'Low', 'Close', 'Volume'])


  # there is a known issue for Google Finance returns wrong value on the 20/11/2017 due the pence and pound conversion
  # e.g LLOY price should be something like 67.33 but return as 0.6733
  # There is no better solution but put a sanity check
  def __dataSanityCheck(self, previous_value, current_value, timestamp, ticker):
    if previous_value > 0.0 and (previous_value - current_value)/ previous_value >= 0.8:
      print("for " + ticker + " there might be a data issue at " + str(timestamp) + " value is " + str(current_value) + " and previous row value is " + str(previous_value))
      current_value = current_value * 100
    return current_value
