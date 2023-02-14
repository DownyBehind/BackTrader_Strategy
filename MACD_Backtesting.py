import backtesting as Backtesting
import yfinance as yf

# Define MACD Strategy
class MACDStrategy(Backtesting.Strategy):
    
    # Define parameters
    params = (("fast", 12), ("slow", 26), ("signal", 9))

    def init(self):
        # Calculate MACD and Signal line
        macd, signal = self.I(macd, self.data.Close, self.params[0], self.params[1], self.params[2])
        self.macd = macd
        self.signal = signal
        
    def next(self):
        # Buy signal when MACD crosses above Signal line
        if self.macd[0] > self.signal[0] and self.macd[-1] <= self.signal[-1]:
            self.buy()
        # Sell signal when MACD crosses below Signal line
        elif self.macd[0] < self.signal[0] and self.macd[-1] >= self.signal[-1]:
            self.sell()

# Define custom MACD function
def macd(close, fast, slow, signal):
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

# Download Yahoo Finance data
data = yf.download("AAPL", start="2010-01-01", end="2022-02-14")

# Create Backtesting object with MACD strategy
bt = Backtesting.Backtest(data, MACDStrategy, cash=10000, commission=0.001)

# Run backtesting and print results
results = bt.run()
print(results)
