import backtrader as bt
import yfinance as yf

class TrendTrader(bt.Strategy):
    params = (
        ('fast_period', 5),
        ('slow_period', 20)
    )
    def __init__(self):
        self.fast_sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.fast_period)
        self.slow_sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.slow_period)
    def next(self):
        if self.fast_sma[0] > self.slow_sma[0] and self.fast_sma[-1] < self.slow_sma[-1]:
            self.buy()
        elif self.fast_sma[0] < self.slow_sma[0] and self.fast_sma[-1] > self.slow_sma[-1]:
            self.sell()

cerebro = bt.Cerebro()

data0 = bt.feeds.PandasData(dataname= yf.download('AAPL','2019-01-01','2019-12-31'))
cerebro.adddata(data0)

cerebro.addstrategy(TrendTrader)

cerebro.run()

cerebro.plot()