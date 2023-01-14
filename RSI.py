import backtrader as bt
import yfinance as yf

class RSIStrategy(bt.Strategy):
    params = (
        ('period', 14),
        ('buy_level', 70),
        ('sell_level', 30),
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.period)

    def next(self):
        if self.rsi[0] > self.params.buy_level:
            self.buy()
        elif self.rsi[0] < self.params.sell_level:
            self.sell()

cerebro = bt.Cerebro()

data = bt.feeds.PandasData(dataname= yf.download('TSLA','2021-01-01','2021-12-31'))
cerebro.adddata(data)

cerebro.addstrategy(RSIStrategy)

cerebro.run()

cerebro.plot()