# Carshalton - A Trading Strategies test and simulator


## Design

### Modules

* Tobor
  * get the price data via data vendors based on configuration
    * from live session (Google Finance)
    * from past data source (local mock data)
  * make calculations (e.g SMA, KDJ, MACD etc)
  * create feed and push down to the Oracle

* Oracle
  * loads the strategies from the strategy base
  * give buy/sell advice based on position and other condition (watch list or holding list)
  * form an instruction and push down the Tobor

* Hugo
  * listen to Oracle and ready to receive instruction
  * execute the instruction via portfolio object

* Portfolio
  * holds the context of the program such as the watch list, investment size, etc
  * portfolio will be pass to other modules for reference
  * internally has a holding list (per stock) and transaction list (all the buy/sell transaction)
  * by the end of the day
    * calculate profit and loss based on the log transaction
    * write the transaction to a csv file
    * produce chart for each holding

## Required libraries
* pandas
* matplotlib - charting
* pydispatcher - message dispatch and subscribe
* stockstats 0.2.0 - technical indicator calculation (SMA, KDJ etc)



## How to run
* make sure you have installed the above package
* go to command line and type  "py go.py"



# Data Issue
Google Finance has data issue for price on the 20/11/2017


# To do:
* for each holding, generate a chart 
* adding a logger
* write the evaluation result to a txt file
