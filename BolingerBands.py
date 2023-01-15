import backtrader as bt
import yfinance as yf

class BollingerBands(bt.Strategy):
    params = (
        ('period', 10),
        ('devfactor', 2),
    )

    def __init__(self):
        self.bb = bt.indicators.BollingerBands(self.data.close, period=self.params.period, devfactor=self.params.devfactor)

    def next(self):
        if not self.position:
            if self.data.close[0] < self.bb.lines.bot[0]:
                self.buy()
        else:
            if self.data.close[0] > self.bb.lines.top[0]:
                self.close()

cerebro = bt.Cerebro()

data = bt.feeds.PandasData(dataname= yf.download('TSLA','2019-01-01','2021-12-31'))
cerebro.adddata(data)

cerebro.addstrategy(BollingerBands)

cerebro.run()

cerebro.plot()