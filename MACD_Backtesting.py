import pandas as pd
import yfinance as yf
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

class MACDStrategy(Strategy):
    params = (
        ('fast', 12),
        ('slow', 26),
        ('signal', 9),
    )

    def init(self):
        close = pd.Series(self.data.Close)
        macd, signal = self.macd(close, fast = int(self.params[0][1]), slow = int(self.params[1][1]), signal = int(self.params[2][1]))
        self.macd_diff = self.I(macd - signal)

    def next(self):
        if self.macd_diff.crossed_above(0):
            self.buy()
        elif self.macd_diff.crossed_below(0):
            self.sell()

    def macd(self, close, fast, slow, signal):
        exp1 = close.ewm(span=fast, adjust=False).mean()
        exp2 = close.ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=signal, adjust=False).mean()
        return macd, signal

# Download stock data from Yahoo Finance
ticker = "AAPL"
data = yf.download(ticker, start="2020-01-01", end="2021-12-31")

# Initialize the backtest
bt = Backtest(data, MACDStrategy, cash=10000, commission=.002, exclusive_orders=True)

# Run the backtest and print the results
results = bt.run()
print(results)

# Plot the backtest results
bt.plot()
