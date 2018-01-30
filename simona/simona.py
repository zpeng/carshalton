import pandas as pd
from pydispatch import dispatcher
from stockstats import StockDataFrame

from simona.dataVendor.dataVendor import DataVendor
from classes.feed import Feed

class Simona:

  def __init__(self, watchList):
    self.watchList = watchList

    self.dataVendorConfig = {
      'i': "1800", # Interval size in seconds ("86400" = 1 day intervals)
      'x': "LON", # Stock exchange symbol on which stock is traded (ex: "NASD")
      'p': "2d" # Period (Ex: "1Y" = 1 year)
    }
    self.dataVendor = DataVendor('GoogleFinance', self.dataVendorConfig)

    self.dataTableRowSize = 10
    self.dataTables = {} # { 'IMB': pandas.DF }

    self.__initialization()


  def __initialization(self):
    self.__updateData()


  # update all data via looping over tickers , then get dataframe from dataVendor,
  # calculate and update technical indicators then truncate table frame into the size
  # of dataTableRowSize
  def __updateData(self):
    for ticker in self.watchList:
      self.dataTables[ticker] = self.dataVendor.getPriceData(ticker)
      self.dataTables[ticker] = self.__calculateTechnicalIndicator(self.dataTables[ticker])
      self.dataTables[ticker] = self.__updateDataTableSize(self.dataTables[ticker])
      #print(self.dataTables[ticker])


  # no need for keeping all the data, say 10 rows of data is enough
  def __updateDataTableSize(self, dataFrame):
    return dataFrame.tail(self.dataTableRowSize)


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

  def __broadcastFeed(self, feed):
    singal_name = "simona-feed-update"
    dispatcher.send(feed=feed, signal=singal_name, sender='simona')


  def update(self):

    # update data
    self.__updateData()

    #generate feed and publish it
    for ticker in self.watchList:
      # create and assign feed value
      dataTable = self.dataTables[ticker].tail(1)
      feed = Feed()
      for index, row in dataTable.iterrows():
        feed.ticker = ticker
        feed.timestamp = index
        feed.price = row['Close']
        feed.Volume = row['Close']
        feed.kdj_k = row['KDJ_K']
        feed.kdj_d = row['KDJ_D']
        feed.kdj_j = row['KDJ_J']

        #broadcast feed
        self.__broadcastFeed(feed)



