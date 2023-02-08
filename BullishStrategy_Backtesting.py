from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd

# Download stock data from Yahoo Finance
ticker = "AAPL"
data = yf.download(ticker, start="2020-01-01", end="2021-12-31")


class BullishStrategy(Strategy):
    def init(self):
        # set the fast moving average window
        self.fast_ma = self.I(lambda: pd.Series(self.data.Close).rolling(window=10).mean(), 'fast_ma')

        # set the slow moving average window
        self.slow_ma = self.I(lambda: pd.Series(self.data.Close).rolling(window=30).mean(), 'slow_ma')

    def next(self):
        # if fast moving average crosses above slow moving average, buy
        if crossover(self.fast_ma, self.slow_ma):
            self.buy()

# initialize Backtest with data and strategy
bt = Backtest(data, BullishStrategy, commission=.001)

# run the backtest
bt.run()

# view the results
bt.plot()
