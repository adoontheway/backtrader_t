import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds
'''
有默认值的参数都被定义为类属性 tuple 或者 类字典的对象
都可以通过self.params访问到，快捷方式self.p

由于python不能override运算符，所以提供了对应的函数:
And, Or, If,Any, All, Cmp,Max,Min,Sum->实际上使用的是math.fsum, Reduce
'''
class MyStrategy(bt.Strategy):
    # params = dict(period1=20,period2=20,period3=20,period4=20)
    # tuple作为参数
    params = (('period',20))
    def __init__(self) -> None:
        # sample 1
        # self.movav = btind.MovingAverageSimple(self.data,period=self.p.period)
        # sample 2
        # datasum = btind.SumN(self.data,period=self.params.period)
        # av =datasum/self.params.period
        # self.line.sma = av
        # sample 3
        sma = btind.MovingAverageSimple(self.data, period=20)
        close_over_sma = self.data.close > sma
        self.sma_dist_to_high = self.data.high - sma
        sma_dist_small = sma_dist_to_high< 3.5
        self.sell_sig = bt.And(close_over_sma, sma_dist_small)
        pass

    def next(self):
        # if self.movav.lines.sma[0] > self.data.lines.close[0]:
        #     print("Simple Moving Average is greater than the closing price")
        # sample 3
        if self.sma > 30.0:
            print('sma is greater than 30.0')

        if self.sma > self.data.close:
            print('sma is above the close price')

        if self.sell_sig:
            print('sell_sig is True')
        else:
            print('sell sig is Flase')

        if self.sma_dist_to_high > 5.0:
            print('distance from sma to high and is greater than 5.0')