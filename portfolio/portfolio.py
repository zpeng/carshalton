import pandas as pd
import time
from datetime import datetime
import uuid

class Portfolio:

    def __init__(self, config):

        self.name = config['name']
        self.cash = config['cash']
        self.initialInvestment = self.cash
        self.sizePerInvestment = config['sizePerInvestment']
        self.maxProportionPerHolding = config['maxProportionPerHolding']
        self.fee = config['fee']
        self.tax = config['tax']
        self.watchList = config['watchList']  # e.g  ['LLOY','HSBC','IMB']

        self.logbook = pd.DataFrame(columns = ['Timestamp', 'Holding_id', 'Ticker', 'Price', 'Quantity','Consolidation', 'Action', 'Profit', 'Reason'])
        self.holdingDict = {}
        self.transactionList = []

    def getWatchList(self):
        return self.watchList

    # Get current holding list for a particular stock
    def getHoldingListByTicker(self, ticker):
        holdings = []
        for key, holding in self.holdingDict.items():
            if holding['Ticker'] == ticker:
                holdings.append(holding)

        return holdings

    # To buy
    def buy(self, ticker, price, timestamp, reason):
        # if we have enough cash
        if self.hasEnoughCashToInvest:
            quantity = round((self.sizePerInvestment - self.fee) * (1 - self.tax) / price)
            consolidation = price * quantity * (1 + self.tax) + self.fee # cost of buy
            # update cash position
            self.cash = self.cash - consolidation

            # log the transaction
            holding_id = str(uuid.uuid4().hex)
            entry = {
                'Holding_id': holding_id,
                'Timestamp': str(timestamp),
                'Ticker': ticker,
                'Price': price,
                'Quantity': quantity,
                'Consolidation': consolidation,
                'Action': 'Buy',
                'Profit': 0,
                'Reason': reason
            }
            self.transactionList.append(entry)

            # update holding dict
            self.holdingDict[holding_id] = entry

    # To sell
    def sell(self, holding_id, ticker, sell_price, sell_quantity, timestamp, reason):
        previousHolding = self.holdingDict[holding_id]
        self.holdingDict.pop(holding_id) # remove this entry from the holding list
        consolidation = sell_price * sell_quantity - self.fee
        self.cash = self.cash + consolidation  # update cash position
        profit = consolidation - previousHolding['Consolidation']

        # log the transaction
        entry = {
            'Holding_id': holding_id,
            'Timestamp': str(timestamp),
            'Ticker': ticker,
            'Price': sell_price,
            'Quantity': sell_quantity,
            'Consolidation': consolidation,
            'Action': 'Sell',
            'Profit': profit,
            'Reason': reason
        }
        self.transactionList.append(entry)

    # check if we have enough cash to invest
    def hasEnoughCashToInvest(self):
        return self.cash >= self.sizePerInvestment

    def hasReachedMaxPropertionPerHolding(self, ticker):
        result = False
        holdingList = self.getHoldingListByTicker(ticker)
        totalHolding = 0.0
        for holding in holdingList:
            totalHolding = totalHolding + holding['Consolidation']
        pct = totalHolding / self.__getPortfolioSize()
        if pct >= self.maxProportionPerHolding:
            result = True
        return result

    def showStats(self):
        print('***********************************************************')
        print('Portfolio: ' + self.name)
        print('Initial Investment: ' + str(self.initialInvestment))
        print('Cash in hand: ' + str(self.cash))
        print("Overall Profit: " + str(self.__getOverallProfit()))
        print("Overall Profit %: " + str(self.__getOverallProfit() / self.initialInvestment * 100))
        print('***********************************************************')


    def evaluation(self):
        self.__writeToLogbook()

    def __getOverallProfit(self):
        totalProfit = 0.0
        for trans in self.transactionList:
            totalProfit = totalProfit + trans['Profit']
        return totalProfit


    def __getPortfolioSize(self):
        size = 0.0
        for key, holding in self.holdingDict.items():
            size = size + holding['Consolidation']
        size = size + self.cash
        return size


    def __writeToLogbook(self):
        for entry in self.transactionList:
            self.logbook = self.logbook.append(entry, ignore_index=True)

        self.logbook.at['Sum', 'Profit'] = self.logbook['Profit'].sum()
        self.logbook.at['% Change', 'Profit'] = self.logbook['Profit'].sum() / self.initialInvestment * 100

        file_name = self.name + " - result"  + '.csv'
        self.logbook.to_csv(file_name, encoding='utf-8')

