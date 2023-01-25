import backtrader as bt
import yfinance as yf

class MultiIndicatorStrategy(bt.Strategy):
    params = (
        ('sma1_period', 20),
        ('sma2_period', 50),
        ('rsi_period', 7),
        ('rsi_oversold', 40),
        ('rsi_overbought', 60),
    )

    def __init__(self):
        self.sma1 = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.sma1_period)
        self.sma2 = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.sma2_period)
        self.rsi = bt.indicators.RelativeStrengthIndex(self.data.close, period=self.params.rsi_period)

    def next(self):
        if not self.position:
            if self.sma1[0] > self.sma2[0] and self.rsi[0] < self.params.rsi_oversold:
                self.buy()
        else:
            if self.sma1[0] < self.sma2[0] or self.rsi[0] > self.params.rsi_overbought:
                self.close()

cerebro = bt.Cerebro()

data = bt.feeds.PandasData(dataname= yf.download('TSLA','2018-01-01','2021-12-31'))
cerebro.adddata(data)

cerebro.addstrategy(MultiIndicatorStrategy)

cerebro.run()

cerebro.plot()
