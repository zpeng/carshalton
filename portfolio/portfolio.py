import pandas as pd
import time
from datetime import datetime
import uuid
from io import StringIO
import glob, os, os.path
import matplotlib.pyplot as plt

class Portfolio:

    def __init__(self, config, dataSource):

        self.name = config['name']
        self.cash = config['cash']
        self.initialInvestment = self.cash
        self.sizePerInvestment = config['sizePerInvestment']
        self.maxNumHoldingsPerStock = config['maxNumHoldingsPerStock']
        self.fee = config['fee']
        self.tax = config['tax']
        self.watchList = config['watchList']  # e.g  ['LLOY','HSBC','IMB']

        self.logbook = pd.DataFrame(columns = ['Timestamp', 'Holding_id', 'Ticker', 'Price', 'Quantity','Consolidation', 'Action', 'Profit', 'Reason'])

        # each holding has an id for referencing
        self.openedHoldings = {}
        self.closedHoldings = {}
        self.transactionList = []

        self.dataSource = dataSource

        # other config
        self.resultFolderPath = './result/'

    def getWatchList(self):
        return self.watchList


    def getOpenedHoldingListByTicker(self, ticker):
        holdingList = []
        for key, holding in self.openedHoldings.items():
            if holding['Ticker'] == ticker:
                holdingList.append(holding)

        return holdingList

    def getCloseHoldingListByTicker(self, ticker):
        holdingList = []
        for key, holding in self.closedHoldings.items():
            if holding['Ticker'] == ticker:
                holdingList.append(holding)

        return holdingList

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

            # update opened holding dict
            self.openedHoldings[holding_id] = entry

    # To sell
    def sell(self, holding_id, ticker, sell_price, sell_quantity, timestamp, reason):
        previousHolding = self.openedHoldings[holding_id]
        self.openedHoldings.pop(holding_id) # remove this entry from the holding list
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
        self.closedHoldings[holding_id] = entry
        self.transactionList.append(entry)

    # check if we have enough cash to invest
    def hasEnoughCashToInvest(self):
        return self.cash >= self.sizePerInvestment

    def hasReachedMaxNumHoldingsPerStock(self, ticker):
        result = False
        n = len(self.getOpenedHoldingListByTicker(ticker))
        if n >= self.maxNumHoldingsPerStock:
            result = True
        return result

    def evaluation(self):
        self.__cleanResultFolder()
        self.__savePortfolioResult()
        self.__writeToLogbook()
        self.__generateCharts()

    def __getTransactionListByTicker(self, ticker):
        transList = []
        for trans in self.transactionList:
            if trans['Ticker'] == ticker: transList.append(trans)
        return transList

    def __getOverallProfit(self):
        totalProfit = 0.0
        for trans in self.transactionList:
            totalProfit = totalProfit + trans['Profit']
        return totalProfit

    def __getPortfolioSize(self):
        size = 0.0
        for key, holding in self.openedHoldings.items():
            size = size + holding['Consolidation']
        size = size + self.cash
        return size

    def __writeToLogbook(self):
        for entry in self.transactionList:
            self.logbook = self.logbook.append(entry, ignore_index=True)

        self.logbook.at['Sum', 'Profit'] = self.logbook['Profit'].sum()
        self.logbook.at['% Change', 'Profit'] = self.logbook['Profit'].sum() / self.initialInvestment * 100

        file_name = self.resultFolderPath + self.name + " - result"  + '.csv'
        self.logbook.to_csv(file_name, encoding='utf-8')

    def __savePortfolioResult(self):
        file_name = self.name + " - result"  + '.txt'
        f = open('./result/' + file_name,'w')
        self.__generatePortfolioStatsInStringIO(f)
        f.close()

    def __generatePortfolioStatsInStringIO(self, output):
        now = datetime.now()
        output.write('********************** Result ***************************\n')
        output.write('Portfolio: ' + self.name + '\n')
        output.write('Test finish at: ' + now.strftime("%Y-%m-%d %H:%M") + '\n')
        output.write('Initial Investment: ' + str(self.initialInvestment) +'\n')
        output.write('Watch List: ' + ', '.join(self.watchList) + '\n')
        output.write('No of stock to Watch: ' + str(len(self.watchList)) + '\n')
        output.write('Cash in hand: ' + str(self.cash) + '\n')
        output.write("Overall Profit: " + str(self.__getOverallProfit()) + '\n')
        output.write("Overall Profit %: " + str(self.__getOverallProfit() / self.initialInvestment * 100) + '\n')
        output.write('Total No of trades: ' + str(len(self.transactionList)) + '\n')
        output.write("\n")
        output.write("--------- Closed Holdings --------\n")
        for ticker in self.getWatchList():
            self.__generateClosedHoldingStatsInStringIO(ticker, output)

        output.write("\n")
        output.write("--------- Current Holdings -----------\n")
        for key, holding in self.openedHoldings.items():
            output.write("Ticker:" + holding['Ticker'] + '  Price:' + str(holding['Price']) + '  Quantity:'+str(holding['Quantity']) + '\n')
        output.write('***********************************************************\n')

    def __generateClosedHoldingStatsInStringIO(self, ticker, outputIO):
        num_trans = 0
        total_profit = 0
        total_solidation = 0
        profit_p = 0
        holdingList = self.getCloseHoldingListByTicker(ticker)
        num_trans = len(holdingList) * 2 # if there is a sell, there always be a buy
        for entry in holdingList:
            total_solidation = total_solidation + entry['Consolidation'] - entry['Profit']
            total_profit = total_profit + entry['Profit']
        if (total_solidation > 0): profit_p = total_profit / total_solidation * 100
        outputIO.write('Ticker: ' + ticker + '\n')
        outputIO.write('Profit: ' + str(total_profit) + '\n')
        outputIO.write('Profit %: ' + str(profit_p) + '\n')
        outputIO.write('Overall Size of Investment: ' + str(total_solidation) + '\n')
        outputIO.write('Number of Trades: ' + str(num_trans) + '\n')
        outputIO.write('\n')

    def __generateCharts(self):
       for ticker in self.watchList:
           self.__plotAndSaveChartForTicker(ticker)

    def __plotAndSaveChartForTicker(self, ticker):
        # process the original dataTable again
        data = self.dataSource.getDataTableByTicker(ticker)
        data = data.assign(Action = '')
        data = data.assign(Reason = '')
        transList = self.__getTransactionListByTicker(ticker)
        for trans in transList:
            data.loc[data['Timestamp'] == trans['Timestamp'], 'Action'] = trans['Action']
            data.loc[data['Timestamp'] == trans['Timestamp'], 'Reason'] = trans['Reason']
        data.set_index('Timestamp',inplace=True)

        # plot and save chart
        fig = plt.figure()
        fig.patch.set_facecolor('white')     # Set the outer colour to white
        ax1 = fig.add_subplot(111, ylabel='', title=ticker)
        data['Close'].plot(ax=ax1, color='dodgerblue', lw=1.,  grid = True, label='Close Price').set_xlabel('')
        ax1.plot(data.loc[data['Action'] == 'Buy'].index, data.Close[data['Action'] == 'Buy'], marker='o', markersize=6, color='green', linestyle='', label='Buy')
        ax1.plot(data.loc[data['Action'] == 'Sell'].index, data.Close[data['Action'] == 'Sell'], marker='s', markersize=6, color='red', linestyle='', label='Sell')
        ax1.legend()
        ax1.autoscale_view()

        img_path = self.resultFolderPath + ticker + ".png"
        plt.savefig(img_path, format='png', dpi=1200)
        plt.close(fig)

        # save the dataTable dump
        file_path = self.resultFolderPath + ticker + ".csv"
        data.to_csv(file_path, encoding='utf-8')

    def __cleanResultFolder(self):
        filelist = glob.glob(os.path.join(self.resultFolderPath, "*.csv"))
        for f in filelist:
            os.remove(f)

        filelist = glob.glob(os.path.join(self.resultFolderPath, "*.png"))
        for f in filelist:
            os.remove(f)

        filelist = glob.glob(os.path.join(self.resultFolderPath, "*.txt"))
        for f in filelist:
            os.remove(f)



