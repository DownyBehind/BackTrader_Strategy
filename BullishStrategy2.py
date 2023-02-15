import backtrader as bt
import yfinance as yf


class MyStrategy(bt.Strategy):
    
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
    
    def next(self):
        if self.order:
            return  # if an order is pending, don't do anything

        if not self.position:  # if not in the market
            if self.dataclose[0] > self.dataclose[-1]:  # if the current close is greater than the previous close
                self.buy()  # enter a long position
        else:
            if self.dataclose[0] < self.dataclose[-1]:  # if the current close is less than the previous close
                self.sell()  # exit the long position

cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)

# Add data feed to cerebro
data = bt.feeds.PandasData(dataname= yf.download('TSLA','2018-01-01','2021-12-31'))
cerebro.adddata(data)

cerebro.run()
cerebro.plot()
