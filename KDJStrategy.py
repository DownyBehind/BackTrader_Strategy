import backtrader as bt
import yfinance as yf



class MyStrategy(bt.Strategy):
    
    def __init__(self):
        self.stock = self.datas[0]
        self.order = None
        self.kdj = bt.indicators.Stochastic(self.stock, period=14, period_dfast=3, period_dslow=3)
        self.sma = bt.indicators.SimpleMovingAverage(self.stock, period=200)

    def next(self):
        if self.order:
            return  # if an order is pending, don't do anything

        if not self.position:  # if not in the market
            if self.kdj.lines.percK[0] > 20 and self.kdj.lines.percD[0] > 20 and (3 * self.kdj.lines.percD[0] - 2 * self.kdj.lines.percK[0]) > 20 and self.stock.close[0] > self.sma[0]:
                self.buy()  # enter a long position
        else:
            if self.kdj.lines.percK[0] < 80 and self.kdj.lines.percD[0] < 80 and (3 * self.kdj.lines.percD[0] - 2 * self.kdj.lines.percK[0]) < 80:
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
