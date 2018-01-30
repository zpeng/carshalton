import pandas as pd

class MockDataSource:

  def __init__(self, config):

    self.config = config

    self.dataTables = {}
    self.__loadDataFromCSV()


  def __loadDataFromCSV(self):
    for k, v in self.config.items():
      self.dataTables[k] = pd.read_csv('./tobor/mock_data/'+v , encoding='utf-8')


  def readDataRange(self, ticker, start, end):
    data = self.dataTables[ticker].iloc[start : end]
    return data



