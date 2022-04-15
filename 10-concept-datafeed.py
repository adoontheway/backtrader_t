import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds
'''
所有基础工作都是由Strategies完成，
策略需要接受数据流 Data Feeds，
终端用于不需要察觉数据流的存在
'''
class MyStrategy(bt.Strategy):
    params = dict(period1=20,period2=20,period3=20,period4=20)
    def __init__(self) -> None:
        # self.datas是数组/列表/可迭代，最少要有一条数据，不然会报错
        sma1 = btind.MovingAverageSimple(self.datas[0],period=self.params.period1)
        # self.data -> self.datas[0], self.dataX -> self.datas[x]
        # sma = btind.MovingAverageSimple(self.data,period=self.params.period)
        # sma = btind.MovingAverageSimple(period=self.params.period)
        # 基本上所有东西都是Data Feed，Indicator和 操作结果也是data
        
        # 第二个SMA操作用sma1作为data
        sma2 = btind.MovingAverageSimple(sma1, period=self.params.period2)

        # 运算操作产生的新data
        something = sma2 - sma1 + self.data.close
        
        sma3 = btind.MovingAverageSimple(something, period=self.params.period3)

        # 比较运算也可以作为data
        greater = sma3 > sma1
        
        sma3= btind.MovingAverageSimple(greater,period=self.params.period4)