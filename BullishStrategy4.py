import backtrader as bt
import yfinance as yf



class MyStrategy(bt.Strategy):
    
    def __init__(self):
        self.sp500 = self.datas[0]
        self.stock = self.datas[1]
        self.order = None
        self.sp500_sma = bt.indicators.SMA(self.sp500.close, period=50)

    def next(self):
        if self.order:
            return  # if an order is pending, don't do anything

        if not self.position:  # if not in the market
            if self.sp500.close[0] > self.sp500_sma[0]:  # if the current S&P 500 close is greater than its 200-day moving average
                self.buy()  # enter a long position
        else:
            if self.sp500.close[0] < self.sp500_sma[0]:  # if the current S&P 500 close is less than its 200-day moving average
                self.sell()  # exit the long position


cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)

# Add data feed to cerebro
nasdaq_data = bt.feeds.PandasData(dataname= yf.download('^GSPC','2018-01-01','2021-12-31'))
data = bt.feeds.PandasData(dataname= yf.download('TSLA','2018-01-01','2021-12-31'))

cerebro.adddata(nasdaq_data)
cerebro.adddata(data)

cerebro.run()
cerebro.plot()
