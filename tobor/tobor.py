import pandas as pd
from pydispatch import dispatcher
from stockstats import StockDataFrame

from tobor.mockDataSource import MockDataSource
from classes.feed import Feed
from portfolio.portfolio import Portfolio

class Tobor:

  def __init__(self, config, portfolio):

    self.mockDataSource = MockDataSource(config['data_source'])

    self.portfolio = portfolio

    self.tableRowSize = 10
    self.dataReadIndex = self.tableRowSize # reads data from index 10
    self.dataTables = {} # { 'IMB': pandas.DF }

    self.__initialization()


  def __initialization(self):
    self.__updateDataTables()


  # calculate Technical Indicators and assign values to the dataFrame
  def __calculateTechnicalIndicator(self, dataFrame):
    stockstatsData = StockDataFrame.retype(dataFrame.copy())
    kdjk = stockstatsData['kdjk']
    kdjd = stockstatsData['kdjd']
    kdjj = stockstatsData['kdjj']
    dataFrame['KDJ_K'] = kdjk
    dataFrame['KDJ_D'] = kdjd
    dataFrame['KDJ_J'] = kdjj
    return dataFrame

  # update data
  def __updateDataTables(self):
    for ticker in self.portfolio.getWatchList():
      self.dataTables[ticker] = self.mockDataSource.readDataRange(ticker, self.dataReadIndex - self.tableRowSize , self.dataReadIndex)
      self.dataTables[ticker] = self.__calculateTechnicalIndicator(self.dataTables[ticker])

  def __broadcastFeed(self, feed):
    singal_name = "tobor-feed-update"
    dispatcher.send(feed=feed, signal=singal_name, sender='tobor')
    #print("feed sent by Tobor")

  def update(self):
    self.dataReadIndex += 1
    self.__updateDataTables()

    #generate feed and publish it
    for ticker in self.portfolio.getWatchList():
      # create and assign feed value
      dataTable = self.dataTables[ticker].tail(1)
      feed = Feed()
      for index, row in dataTable.iterrows():
        feed.ticker = ticker
        feed.timestamp = row['Timestamp']
        feed.price = row['Close']
        feed.Volume = row['Volume']
        feed.kdj_k = row['KDJ_K']
        feed.kdj_d = row['KDJ_D']
        feed.kdj_j = row['KDJ_J']

        #broadcast feed
        self.__broadcastFeed(feed)


