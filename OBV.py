import backtrader as bt
import yfinance as yf

class MyStrategy(bt.Strategy):
    
    def __init__(self):
        self.stock = self.datas[0]
        self.order = None
        self.vwma = bt.indicators.WMA(self.stock, period=20)

    def next(self):
        if self.order:
            return  # if an order is pending, don't do anything

        if not self.position:  # if not in the market
            if self.stock.close[0] > self.vwma[0]:  # if the current close price is greater than the VWMA
                self.buy()  # enter a long position
        else:
            if self.stock.close[0] < self.vwma[0]:  # if the current close price is less than the VWMA
                self.sell()  # exit the long position


cerebro = bt.Cerebro()

data = bt.feeds.PandasData(dataname= yf.download('TSLA','2018-01-01','2021-12-31'))
cerebro.adddata(data)

cerebro.addstrategy(MyStrategy)

cerebro.run()

cerebro.plot()
