import backtrader as bt
import yfinance as yf

class ReverseTrend(bt.Strategy):
    params = (
        ('fast_ma_period', 10),
        ('slow_ma_period', 30),
        ('stop_loss', 0.03),
        ('take_profit', 0.05),
    )

    def __init__(self):
        self.fast_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.fast_ma_period)
        self.slow_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.slow_ma_period)
        
        self.order = None
        self.stop_price = None
        self.take_price = None

    def next(self):
        if self.order:
            if self.data.close[0] >= self.take_price or \
               self.data.close[0] <= self.stop_price:
                self.sell()
            return

        if self.fast_ma[0] < self.slow_ma[0] and \
           self.fast_ma[-1] > self.slow_ma[-1]:
            self.order = self.buy()
            self.stop_price = self.data.close[0] * (1.0 - self.params.stop_loss)
            self.take_price = self.data.close[0] * (1.0 + self.params.take_profit)


cerebro = bt.Cerebro()

data = bt.feeds.PandasData(dataname= yf.download('TSLA','2021-01-01','2021-12-31'))
cerebro.adddata(data)

cerebro.addstrategy(ReverseTrend)

cerebro.run()

cerebro.plot()
