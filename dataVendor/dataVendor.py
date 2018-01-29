import pandas as pd
from dataVendor.googleFinance import GoogleFinance

class DataVendor:

  def __init__(self, vendorName, config):
    if vendorName == '': vendorName = 'GoogleFinance'
    self.vendorName = vendorName
    self.config = {}

    if self.vendorName == 'GoogleFinance':
      self.config['i'] = config['i']
      self.config['x'] = config['x']
      self.config['p'] = config['p']
      self.vendor = GoogleFinance(self.config)

  def getPriceData(self, ticker):
    data = self.vendor.getPriceData(ticker)
    return data

  def getLatestPriceData(self, ticker):
    data = self.vendor.getPriceData(ticker)
    # only return the last one
    return data.tail(1)


