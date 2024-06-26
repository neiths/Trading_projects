import backtrader as bt
from typing import Union

def init_cerebro_object(strategy, list_of_data, cash=20000):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy)
    for data in list_of_data:
        cerebro.adddata(data)
    cerebro.broker.set_cash(cash)
    return cerebro

def run_cerebro(strategy, list_data, stake=100, cash=20000):
    cerebro = init_cerebro_object(strategy, list_data, cash)
    thestrats = cerebro.run()
    return cerebro, thestrats
