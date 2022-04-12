from __future__ import (absolute_import,division,print_function,unicode_literals)
from audioop import reverse

import datetime
import os.path
import sys

import backtrader as bt

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # Data are in a subfolder of this sample,
    # need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath,'./datas/orcl-1995-2014.txt')

    # Create Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2000,1,1),
        todata=datetime.datetime(2000,12,31),
        reverse=False
    )

    # Add data feed to Cerrbro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value:%.2f'%cerebro.broker.getvalue())

    # Run over
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value:%.2f'%cerebro.broker.getvalue())