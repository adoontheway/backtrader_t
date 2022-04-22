import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds
'''
有默认值的参数都被定义为类属性 tuple 或者 类字典的对象
都可以通过self.params访问到，快捷方式self.p
'''
class MyStrategy(bt.Strategy):
    # params = dict(period1=20,period2=20,period3=20,period4=20)
    # tuple作为参数
    params = (('period',20))
    def __init__(self) -> None:
        sma1 = btind.MovingAverageSimple(self.datas[0],period=self.p.period1)