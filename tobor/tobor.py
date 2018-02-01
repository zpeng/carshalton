import pandas as pd
from pydispatch import dispatcher
from stockstats import StockDataFrame

from tobor.dataSource import DataSource
from classes.feed import Feed
from portfolio.portfolio import Portfolio

class Tobor:

  def __init__(self, ds_config, portfolio):

    dataSource = DataSource(ds_config) # dataSource has loaded up with data

    self.portfolio = portfolio

    self.dataReadIndex = ds_config['startIndex'] # reads data from index 10
    self.dataTables = dataSource.getDataTables()
    self.__initialization()


  def __initialization(self):
    # calculate technical indicators
    for ticker in self.portfolio.getWatchList():
      self.dataTables[ticker] = self.__calculateTechnicalIndicator(self.dataTables[ticker])


  # calculate Technical Indicators and assign values to the dataFrame
  def __calculateTechnicalIndicator(self, dataFrame):
    stockstatsData = StockDataFrame.retype(dataFrame.copy())
    kdjk = stockstatsData['kdjk']
    kdjd = stockstatsData['kdjd']
    kdjj = stockstatsData['kdjj']
    rsi = stockstatsData['rsi_9']
    dataFrame['KDJ_K'] = kdjk
    dataFrame['KDJ_D'] = kdjd
    dataFrame['KDJ_J'] = kdjj
    dataFrame['RSI'] = rsi
    return dataFrame

  def __broadcastFeed(self, feed):
    singal_name = "tobor-feed-update"
    dispatcher.send(feed=feed, signal=singal_name, sender='tobor')
    #print("feed sent by Tobor")

  def update(self):
    self.dataReadIndex += 1

    #generate feed and publish it
    for ticker in self.portfolio.getWatchList():
      # create and assign feed value
      row = self.dataTables[ticker].iloc[self.dataReadIndex]
      feed = Feed()
      feed.ticker = ticker
      feed.timestamp = row['Timestamp']
      feed.price = row['Close']
      feed.Volume = row['Volume']
      feed.kdj_k = row['KDJ_K']
      feed.kdj_d = row['KDJ_D']
      feed.kdj_j = row['KDJ_J']
      feed.rsi = row['RSI']

      #broadcast feed
      self.__broadcastFeed(feed)


