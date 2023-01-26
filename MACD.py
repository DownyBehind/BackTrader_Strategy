import backtrader as bt
import yfinance as yf

class MACDStrategy(bt.Strategy):
    params = (
        ("fast", 12),
        ("slow", 26),
        ("signal", 9),
        ("stop_loss", 0.03),
        ("take_profit", 0.05),
    )

    def __init__(self):
        self.macd = bt.indicators.MACD(
            self.data.close,
            period_me1=self.params.fast,
            period_me2=self.params.slow,
            period_signal=self.params.signal
        )

    def next(self):
        if not self.position:
            if self.macd.macd[0] > self.macd.signal[0]:
                self.buy()
        else:
            if self.macd.macd[0] < self.macd.signal[0]:
                self.sell()

cerebro = bt.Cerebro()

data = bt.feeds.PandasData(dataname= yf.download('TSLA','2018-01-01','2021-12-31'))
cerebro.adddata(data)

cerebro.addstrategy(MACDStrategy)

cerebro.run()

cerebro.plot()
