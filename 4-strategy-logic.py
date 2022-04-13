from __future__ import (
    absolute_import,division,print_function,unicode_literals
)
'''
加入购买逻辑
'''

import datetime
import os.path
import sys

import backtrader as bt

# Create a Strategy
class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Log function '''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s'%(dt.isoformat(), txt))
    
    def __init__(self) -> None:
        # Keep a reference to the 'close' line in the data[0] dateseries
        self.dataclose = self.datas[0].close

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f'%self.dataclose[0])
        if self.dataclose[0] < self.dataclose[-1]:
            # current close less than previous close
            if self.dataclose[-1] < self.dataclose[-2]:
                # previous close less than the previous close
                self.log('BUY CREATE, %.2f'%self.dataclose[0])
                self.buy()

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath,"./datas/orcl-1995-2014.txt")

    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2000,1,1),
        todate=datetime.datetime(2000,12,31),
        reverse=False
    )

    cerebro.adddata(data)

    cerebro.broker.setcash(100000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value:%.2f'%cerebro.broker.getvalue())
    cerebro.run()
    # Print out the final conditions
    print('Final Portfolio Value:%.2f'%cerebro.broker.getvalue())