from datetime import datetime
import backtrader as bt
import yfinance as yf

class MeanReversion(bt.Strategy):
    params = (
        ('period', 20),
        ('devfactor', 2)
    )

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.period)
        self.bbands = bt.indicators.BollingerBands(
            self.data.close, period=self.params.period)

    def next(self):
        if self.data.close[0] < self.bbands.bot[0]:
            self.buy()
        elif self.data.close[0] > self.bbands.top[0]:
            self.sell()

cerebro = bt.Cerebro()

data = bt.feeds.PandasData(dataname= yf.download('TSLA','2021-01-01','2021-12-31'))
cerebro.adddata(data)

cerebro.addstrategy(MeanReversion)

cerebro.run()

cerebro.plot()