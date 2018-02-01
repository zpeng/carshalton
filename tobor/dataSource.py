import pandas as pd
from tobor.googleFinance import GoogleFinance

class DataSource:

  def __init__(self, config):

    self.config = config
    self.dataTables = {}
    self.googleFinance = None

    if config['mode'] == 'mock':
      # load mock data from local CSV files
      self.__loadDataFromCSV(config['mock'])
    elif config['mode'] == 'live':
      # loads data from Google Finance
      self.googleFinance = GoogleFinance(config['live']['gf_config'])
      self.__loadDataFromGoogleFinance(config['live']['tickerList'])

  def getDataTables(self):
    return self.dataTables

  def __loadDataFromGoogleFinance(self, tickerList):
    for ticker in tickerList:
      self.dataTables[ticker] = self.googleFinance.getPriceData(ticker)

  def __loadDataFromCSV(self, mockDataSources):
    for k, v in mockDataSources.items():
      self.dataTables[k] = pd.read_csv('./mock_data/'+v , encoding='utf-8')




