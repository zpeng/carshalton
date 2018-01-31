from pydispatch import dispatcher
from classes.instruction import Instruction
from portfolio.portfolio import Portfolio

class Hugo:
  def __init__(self, portfolio):

    self.portfolio = portfolio

    # event registration
    dispatcher.connect(self.__handleOracleInstruction, signal='oracle-instruction-update', sender='oracle')


  def __handleOracleInstruction(self, instruction):
    if (instruction.action == 'Buy' or instruction.action == 'Sell'):
      print("Hugo has received instruction from Oracle: " + str(instruction.timestamp) + " " + instruction.ticker + " - " + str(instruction.action) + " - " + str(instruction.reason))

    if (instruction.action == 'Buy'):
      # update portfolio
      self.portfolio.buy(instruction.ticker, instruction.price, instruction.timestamp, instruction.reason)


    if (instruction.action == 'Sell'):
      # update portfolio
      self.portfolio.sell(instruction.holding_id, instruction.ticker, instruction.price, instruction.quantity, instruction.timestamp, instruction.reason)

