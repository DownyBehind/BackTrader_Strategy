import pandas as pd
import yfinance as yf
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Download stock data from Yahoo Finance
ticker = "AAPL"
data = yf.download(ticker, start="2020-01-01", end="2021-12-31")

# Define a simple moving average crossover strategy
class SmaCross(Strategy):
    def init(self):
        self.sma1 = self.I(lambda: pd.Series(self.data.Close).rolling(window=10).mean())
        self.sma2 = self.I(lambda: pd.Series(self.data.Close).rolling(window=20).mean())
    
    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()

# Initialize the backtest
bt = Backtest(data, SmaCross, cash=10000, commission=.002, exclusive_orders=True)

# Run the backtest and print the results
results = bt.run()
print(results)

bt.plot()
