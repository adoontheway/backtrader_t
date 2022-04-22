import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds
'''
让策略跑起来需要至少三个线对象：
数据流
策略：也及时继承自Strategy的类
Cerebro：西班牙语里面大脑的意思
'''

'''
数据流也就是用于通过施加计算来回测的数据
此平台提供了一些数据：
    一些csv和通用的csv reader
    yahoo在线拉取
    支持接收Pandas Dataframe和blaze对象
    来自Interacive Brokers，Visual Charts和Oanda的实时数据流
平台不会对数据内容进行任何的假设，例如时间帧，压缩等。
这些值都有一个名字，可以用于信息提取和高级操作，如Data Feed Resampling数据流重采样，
'''

# 之前的例子中已经设置Yahooshi财经数据流的
datapath = 'path/to/yahoo/csv'
data = btfeeds.YahooFinanceCSVData(
    dataname=datapath,
    reversed=True # csv文件是直接通过Yahoo最新日期下载的，不是最旧日期
)

# 如果数据时间跨度很大，实际加载数据可以做如下限制
data = btfeeds.YahooFinanceCSVData(
    dataname = datapath,
    reversed = True,
    fromdate = datetime.datetime(2014,1,1),# 将会包含此日期
    todate = datetime.datetime(2014,12,31),# 将会包含此日期
    # 指定时间帧，压缩，名字，在进行plot的时候这些值都会用得上
    timeframe = bt.TimeFrame.Days,# timeframe
    compression = 1, # 是否压缩
    name= 'Yahoo' # 名字
)

'''
backtrader平台的主要功能就是回测，回测都是通过Strategy实现的，
自定义Strategy最少要有两个方法:
__init__ 初始化数据的指示器和其他计算操作以备后用
next 用于处理每条bar

如果不同时间帧的数据传入到next，也就是不同数量的bars，
将会调用主data（第一个传给cerebro的数据），也就是时间帧最小的数据

如果用到了数据重演 Data Replay方法，那么由于bar的开发重演，next方法将会在一个bar上多次被调用
'''
class MyStrategy(bt.Strategy):
    def __init__(self) -> None:
        super().__init__()
    def next(self):
        pass
    def start(self):
        pass
    def stop(self):
        return super().stop()
    # 需要一个买/卖
    def notify_order(self, order):
        return super().notify_order(order)