# Carshalton - A Trading Strategies test and simulator


## Design

### Modules

* Simona
  * get the price data via data vendors based on configuration
    * from live session (Google Finance)
    * from past data source (local mock data)
  * make calculations (e.g SMA, KDJ, MACD etc)
  * create feed and push down to the Oracle

* Oracle
  * loads the strategies from the strategy base (Tank)
  * give buy/sell advice based on position and other condition (watch list or holding list)
  * form an instruction and push down the Executor

* Executor (Better name TBD)
  * execute the instruction
  * log the transaction


* Evaluator
  * calculate profit and loss based on the log transaction


## Required libraries
* pandas
* pydispatcher - message dispatch and subscribe
* stockstats 0.2.0
  * technical indicator calculation (SMA, KDJ etc)


