import backtrader as bt
import yfinance as yf


class VolatilityBreakout(bt.Strategy):
    params = (
        ('atr_period', 7),
        ('stop_loss_factor', 5),
        ('take_profit_factor', 1)
    )

    def __init__(self):
        self.atr = bt.indicators.ATR(self.data, period=self.params.atr_period)
        self.stop_loss_factor = self.params.stop_loss_factor
        self.take_profit_factor = self.params.take_profit_factor
        # self.take_profit = bt.indicators.TakeProfit(self.data, period=self.params.atr_period, factor=self.params.take_profit_factor)
        self.stop_loss_level = None
        self.take_profit_level = None
        self.order = None

    def next(self):
        if not self.position:
            if self.data.high[0] > self.data.close[-1] + self.atr[-1]:
                self.stop_loss_level = self.data.close[-1] - (self.stop_loss_factor * self.atr[-1])
                self.take_profit_level = self.data.close[-1] + (self.take_profit_factor * self.atr[-1])
                self.order = self.buy()
        else:
            if self.data.low[0] < self.stop_loss_level:
                self.close()
            elif self.data.high[0] > self.take_profit_level:
                self.close()

cerebro = bt.Cerebro()

data = bt.feeds.PandasData(dataname= yf.download('TSLA','2021-01-01','2021-12-31'))
cerebro.adddata(data)

cerebro.addstrategy(VolatilityBreakout)

cerebro.run()

cerebro.plot()