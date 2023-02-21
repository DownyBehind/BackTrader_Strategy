import backtrader as bt
import yfinance as yf



class MyStrategy(bt.Strategy):
    
    def __init__(self):
        self.stock = self.datas[0]
        self.order = None
        self.ichimoku = bt.indicators.Ichimoku(self.stock)

    def next(self):
        if self.order:
            return  # if an order is pending, don't do anything

        if not self.position:  # if not in the market
            if self.stock.close[0] > self.ichimoku.senkou_span_a[0] and self.ichimoku.tenkan_sen[0] > self.ichimoku.kijun_sen[0]:
                self.buy()  # enter a long position
        else:
            if self.stock.close[0] < self.ichimoku.senkou_span_b[0]:
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
