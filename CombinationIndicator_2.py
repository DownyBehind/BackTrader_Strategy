import backtrader as bt
import yfinance as yf

class BollingerBandsRSI(bt.Strategy):
    params = (
        ('period', 20),
        ('devfactor', 2),
        ('rsi_period', 14),
        ('rsi_oversold', 30),
        ('rsi_overbought', 70),
    )

    def __init__(self):
        self.bb = bt.indicators.BollingerBands(self.data.close, period=self.params.period, devfactor=self.params.devfactor)
        self.rsi = bt.indicators.RelativeStrengthIndex(self.data.close, period=self.params.rsi_period)

    def next(self):
        if not self.position:
            if self.data.close[0] < self.bb.lines.bot[0] and self.rsi[0] < self.params.rsi_oversold:
                self.buy()
        else:
            if self.data.close[0] > self.bb.lines.top[0] or self.rsi[0] > self.params.rsi_overbought:
                self.close()


cerebro = bt.Cerebro()

data = bt.feeds.PandasData(dataname= yf.download('TSLA','2018-01-01','2021-12-31'))
cerebro.adddata(data)

cerebro.addstrategy(BollingerBandsRSI)

cerebro.run()

cerebro.plot()
