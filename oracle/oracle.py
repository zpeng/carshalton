from pydispatch import dispatcher
from classes.feed import Feed
from portfolio.portfolio import Portfolio
from classes.instruction import Instruction
from oracle.strategies import str_sell_kdj, str_buy_kdj
import copy

class Oracle:
  def __init__(self, portfolio):
    self.portfolio = portfolio

    # event registration
    dispatcher.connect(self.__handleSimonaFeedUpdate, signal='simona-feed-update', sender='simona')
    dispatcher.connect(self.__handleToborFeedUpdate, signal='tobor-feed-update', sender='tobor')


  def __handleSimonaFeedUpdate(self, feed):
    #print("Oracle has received feed from Simona since last update")
    #print(str(feed.timestamp) + " " + feed.ticker + " - " + str(feed.price))
    self.__think(feed)

  def __handleToborFeedUpdate(self, feed):
    #print("Oracle has received feed from Tobor since last update")
    #print(str(feed.timestamp) + " " + feed.ticker + " - " + str(feed.price))
    self.__think(feed)


  def __think(self, feed):
    # perform sell strategies check
    # the holding list need a deep copy as it might be changed by Hugo
    holdingList = copy.deepcopy(self.portfolio.getHoldingListByTicker(feed.ticker))
    for holding in holdingList:
      instruction = Instruction()
      instruction.ticker = feed.ticker
      instruction.timestamp = feed.timestamp
      instruction.price = feed.price
      instruction.quantity = holding['Quantity']
      instruction.action = 'Hold'
      instruction.reason = ''
      instruction.holding_id = holding['Holding_id']

      instruction = str_sell_kdj(feed, holding, instruction)
      self.__broadcastFeed(instruction)

    # perform buy strategies check
    # we have enough cash to buy
    if self.portfolio.hasEnoughCashToInvest() and (not self.portfolio.hasReachedMaxPropertionPerHolding(feed.ticker)):
      instruction = Instruction()
      instruction.ticker = feed.ticker
      instruction.timestamp = feed.timestamp
      instruction.price = feed.price
      instruction.action = 'Hold'
      instruction.reason = ''

      instruction = str_buy_kdj(feed, instruction)
      self.__broadcastFeed(instruction)

  def __broadcastFeed(self, instruction):
    singal_name = "oracle-instruction-update"
    dispatcher.send(instruction=instruction, signal=singal_name, sender='oracle')
