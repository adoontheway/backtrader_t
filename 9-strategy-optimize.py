from __future__ import (
    absolute_import,division,print_function,unicode_literals
)

from matplotlib import style

'''
优化
'''

import datetime
import os.path
import sys
import backtrader as bt

# Commission 佣金
# Create a Strategy
class TestStrategy(bt.Strategy):
    params = (
        ('printlog', False),
        ('maperiod',15),
    )
    def log(self, txt, dt=None, doprint=False):
        ''' Log function '''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s'%(dt.isoformat(), txt))
    
    def __init__(self) -> None:
        # Keep a reference to the 'close' line in the data[0] dateseries
        self.dataclose = self.datas[0].close
        # To keep track of pending orders
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # 添加一个 MovingAverageSimple 指示器
        self.sma = bt.indicators.MovingAverageSimple(
            self.datas[0],
            period=self.params.maperiod
        )

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
            if self.dataclose[0] > self.sma[0]:
                # previous close less than the previous close
                self.log('BUY CREATE, %.2f'%self.dataclose[0])
                # 追踪当前订单以避免生成第二个订单
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.sma[0]:
                # SELL, with all possible default parameters
                self.log("SELL CREATE, %.2f"%self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
    
    def stop(self):
        ''' 当数据用完，回测结束的时候，会调用此方法，此方法用于打印broker里的投资组合的净值 '''
        self.log('(MA period %2d) Ending Value %.2f'%(self.params.maperiod,self.broker.getvalue()),doprint=True)

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # cerebro.addstrategy(TestStrategy)
    # 发生错误 AttributeError: module 'collections' has no attribute 'Iterable'
    # 这个可能跟python版本有关系：Python 3.9 have been deprecated Iteralbe from collections.
    # 需要将版本降级为3.8
    strats = cerebro.optstrategy(
        TestStrategy,
        maperiod=range(10,31))

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath,"./datas/orcl-1995-2014.txt")

    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2000,1,1),
        todate=datetime.datetime(2000,12,31),
        reverse=False
    )

    cerebro.adddata(data)

    cerebro.broker.setcash(1000.0)
    # addsizer
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    # set commission 0.1%
    cerebro.broker.setcommission(commission=0.00)
    

    # Print out the starting conditions
    # print('Starting Portfolio Value:%.2f'%cerebro.broker.getvalue())
    cerebro.run(maxcpu=1)
    # cannot import name 'warnings' from 'matplotlib.dates'
    # Solvement 1:需要降级 matplotlib -> 3.2.2
    # cerebro.plot()
    # Solvement 2: 使用backtrader_plotting替换
    # b = Bokeh(style='bar', plot_mode='single', scheme=Tradimo())
    # cerebro.plot(b)

    # Print out the final conditions
    # print('Final Portfolio Value:%.2f'%cerebro.broker.getvalue())

'''
输出：
第一个交易日不是2000-1-3，而是2000-1-24，
这是因为新加入了SMA指示器，
它需要一定量的X bar来生成输出，
本案例中是15，
2000-1-24也就是第15个bar。

Backtrader是假定策略和他的指示器都已经准备好了的，可以开箱即用。
如果指示器没有准备好，没有必要去用来进行生产
'''