import backtrader as bt
import yfinance as yf

class BullishStrategy(bt.Strategy):
    
    def __init__(self):
        self.sma200 = bt.indicators.SimpleMovingAverage(self.data.close, period=200)
        self.sma50 = bt.indicators.SimpleMovingAverage(self.data.close, period=50)
        self.rsi = bt.indicators.RelativeStrengthIndex()

    def next(self):
        if not self.position:
            if self.data.close[0] > self.sma200[0] and self.data.close[0] > self.sma50[0] and self.rsi[0] > 50:
                self.buy()
        else:
            if self.data.close[0] < self.sma50[0]:
                self.close()

cerebro = bt.Cerebro()

data = bt.feeds.PandasData(dataname= yf.download('TSLA','2018-01-01','2021-12-31'))
cerebro.adddata(data)

cerebro.addstrategy(BullishStrategy)

cerebro.run()

cerebro.plot()
