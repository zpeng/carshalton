import pandas as pd
from dataVendor.dataVendor import DataVendor
from simona.simona import Simona
from oracle.oracle import Oracle
import time

watchList = ['IMB', 'LLOY', 'HSBA']
holdingList = []

simona = Simona(watchList)

oracle = Oracle(watchList, holdingList)


while True :
	simona.update()
	time.sleep(5)






