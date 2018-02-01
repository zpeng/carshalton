from classes.feed import Feed
from classes.instruction import Instruction
import math

def str_sell_kdj(feed, holding, instruction):

  target_profit = 0.05
  stop_loss = -0.05
  over_buy_k = 90
  over_buy_j = 105
  breakeven = 0.015

  # if hits the extreme over buy zone (K > 90 or J > 100 ) and pass profit margin
  if ((feed.kdj_k > over_buy_k or feed.kdj_j > over_buy_j) and __profit_margin(holding['Price'], feed.price) > breakeven):
    instruction.action = "Sell"
    instruction.reason = "Reached over-buy zone (kdj_k=" + str(feed.kdj_k) + " - kdj_j=" + str(feed.kdj_j) + ")"

  elif (__profit_margin(holding['Price'], feed.price) >= target_profit):
    instruction.action = "Sell"
    instruction.reason = "Profit taking - Profit exceed " + str(target_profit) + " at " + str(__profit_margin(holding['Price'], feed.price))

  elif (__profit_margin(holding['Price'], feed.price) <= stop_loss):
    instruction.action = "Sell"
    instruction.reason = "Stop loss - Loss exceed " + str(stop_loss) + " at " + str(math.fabs(__profit_margin(holding['Price'], feed.price)))

  return instruction



def str_buy_kdj(feed, instruction):

  over_sell_k = 10
  over_sell_j = -5

  # if hits the extreme over sell zone (K < 10 or J < 0 ) and pass profit margin
  if (feed.kdj_k <= over_sell_k and feed.kdj_j < over_sell_j):
    instruction.action = "Buy"
    instruction.reason = "Reached over-sell zone (kdj_k=" + str(feed.kdj_k) + " - kdj_j=" + str(feed.kdj_j) + ")"

  return instruction



def __profit_margin(buy_price, sell_price):
  return (sell_price - buy_price) / buy_price