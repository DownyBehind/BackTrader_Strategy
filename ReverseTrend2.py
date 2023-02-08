import backtrader as bt
import yfinance as yf

class ReverseTrendStrategy(bt.Strategy):
    
    params = (
        ("fast_window", 12),
        ("slow_window", 26),
        ("macd_window", 9),
        ("macd_threshold", 0.0),
        ("rsi_window", 14),
        ("rsi_threshold", 50),
        ("stop_loss", 2.0),
        ("take_profit", 5.0),
    )

    def __init__(self):
        self.fast_average = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.fast_window
        )
        self.slow_average = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.slow_window
        )
        self.macd = bt.indicators.MACD(
            self.data.close,
            period_me1=self.params.fast_window,
            period_me2=self.params.slow_window,
            period_signal=self.params.macd_window,
        )
        self.rsi = bt.indicators.RelativeStrengthIndex(
            self.data.close, period=self.params.rsi_window
        )

    def next(self):
        if not self.position:
            if self.macd.macd[0] > self.params.macd_threshold and self.rsi[0] > self.params.rsi_threshold:
                self.buy()
        else:
            if self.macd.macd[0] < self.params.macd_threshold or self.rsi[0] < self.params.rsi_threshold:
                self.sell()
            if self.data.close[0] < self.data.close[-1] * (1 - self.params.stop_loss / 100):
                self.sell()
            if self.data.close[0] > self.data.close[-1] * (1 + self.params.take_profit / 100):
                self.sell()


cerebro = bt.Cerebro()

data = bt.feeds.PandasData(dataname= yf.download('TSLA','2021-01-01','2021-12-31'))
cerebro.adddata(data)

cerebro.addstrategy(ReverseTrendStrategy)

cerebro.run()

cerebro.plot()
