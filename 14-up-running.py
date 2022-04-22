import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds
'''

线迭代器:
    next 每次迭代都会调用，线迭代器自动调用的
    prenext，非常规函数，在线迭代器满足最小周期的时候调用
    nextstart，非常规函数，仅在线迭代器满足最小周期的时候调用一次，默认操作是转发调用next，当然是可以重写的

指示器支持批操作模式，不是严格要求的，但是可以大大的节省时间
    once(self, start, end)
        在满足最小周期的时候调用。需要处理处于start，end之间的内部数组
    preonce(self, start, end)
        在最小周期满足之前调用
    oncestart(self, start, end)
        仅在最小周期满足的时候调用一次。默认是转发调用once。

最小周期
'''

class SimpleMovingAverage(bt.Indicator):
    lines = ('sma',)
    params = dict(period=20)

    def __init__(self) -> None:
        super().__init__()

    def prenext(self):
        print('prenext:: current period:',len(self))

    def nextstart(self):
        print('nextstart:: current period:',len(self))
        self.next()

    def next(self):
        print('next:: current period:',len(self))
