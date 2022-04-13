from __future__ import (
    absolute_import,division,print_function,unicode_literals
)

'''
加入佣金
'''

import datetime
import os.path
import sys

import backtrader as bt
# Commission 佣金
# Create a Strategy
class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Log function '''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s'%(dt.isoformat(), txt))
    
    def __init__(self) -> None:
        # Keep a reference to the 'close' line in the data[0] dateseries
        self.dataclose = self.datas[0].close
        # To keep track of pending orders
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepterd to/by broker - Nothong to do
            return
        
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("BUY EXECUTED, Price %.2f, Cost:%.2f, Comm %.2f"%(
                    order.executed.price,
                    order.executed.value,
                    order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log("SELL EXECUTED, Price %.2f, Cost:%.2f, Comm: %.2f"%(
                    order.executed.price,
                    order.executed.value,
                    order.executed.comm
                ) )
            
            self.bar_executed = len(self)
        
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")
        
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f'%(
            trade.pnl,trade.pnlcomm
        ))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f'%self.dataclose[0])

        # Check if an order is penging... if yes, we cannot send a 2nd one
        if self.order != None:
            return

        # Check if we are in the market
        if not self.position:
            # Not yet, we might buy if
            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close
                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close
                    self.log('BUY CREATE, %.2f'%self.dataclose[0])
                    self.buy()
        else:
            # Already in the market .. we might sell
            if len(self) >= (self.bar_executed+5):
                # SELL, with all possible default parameters
                self.log("SELL CREATE, %.2f"%self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

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
    cerebro.broker.setcommission(commission=0.001)

    # Print out the starting conditions
    print('Starting Portfolio Value:%.2f'%cerebro.broker.getvalue())
    cerebro.run()
    # Print out the final conditions
    print('Final Portfolio Value:%.2f'%cerebro.broker.getvalue())