import backtrader as bt
import yfinance as yf

class GoldenDeadCross(bt.Strategy):
    params = (
        ('fast_period', 20),
        ('slow_period', 50),
    )

    def __init__(self):
        self.fast_sma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.fast_period)
        self.slow_sma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.slow_period)

    def next(self):
        if not self.position:
            if self.fast_sma[0] > self.slow_sma[0]:
                self.buy()
        else:
            if self.fast_sma[0] < self.slow_sma[0]:
                self.close()

cerebro = bt.Cerebro()

data = bt.feeds.PandasData(dataname= yf.download('TSLA','2019-01-01','2021-12-31'))
cerebro.adddata(data)

cerebro.addstrategy(GoldenDeadCross)

cerebro.run()

cerebro.plot()