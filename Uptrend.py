import backtrader as bt
import yfinance as yf

class UpTrend(bt.Strategy):
    params = (
        ('fast_ma_period', 20),
        ('slow_ma_period', 50),
    )

    def __init__(self):
        self.fast_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.fast_ma_period)
        self.slow_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.slow_ma_period)

    def next(self):
        if self.data.close[0] > self.fast_ma[0] and self.data.close[0] > self.slow_ma[0]:
            if not self.position:
                self.buy()
        elif self.data.close[0] < self.fast_ma[0] or self.data.close[0] < self.slow_ma[0]:
            if self.position:
                self.sell()

cerebro = bt.Cerebro()

data = bt.feeds.PandasData(dataname= yf.download('TSLA','2018-01-01','2021-12-31'))
cerebro.adddata(data)

cerebro.addstrategy(UpTrend)

cerebro.run()

cerebro.plot()
