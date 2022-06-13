from datetime import datetime
from time import sleep
import talib as ta
import yfinance as yf



class AutoTrade:
    def __init__(self, auto: bool = True, **kwargs):
        """
        :param kwargs: symbol, client, data, auto
        """
        self.symbol = kwargs.get('symbol', 'BTC-USD')
        self.prices = None
        self.prime_signal = None
        self.rsi = None
        self.macd = None
        self.stock = None
        self.client = kwargs.get('client', None)
        self.auto = auto

    @staticmethod
    def time():
        date_time = datetime.utcnow()
        return date_time

    def get_prices(self) -> None:
        """
        Getting the data if None was Provided
        """
        btc = yf.Ticker(self.symbol)
        self.prices = btc.history(period='3d', interval='30m')

    def cal_indicators(self) -> None:
        """
        Calculating the indicators from the data
        4 indicators MACD, RSI, Stochastic, Bollinger Bands

        """
        self.get_prices()
        self.prices['rsi'] = ta.RSI(self.prices['Close'], timeperiod=20)
        self.prices['macd'], self.prices['macd_signal'], self.prices['histogram'] = ta.MACD(self.prices['Close'],
                                                                                            fastperiod=8,
                                                                                            slowperiod=21,
                                                                                            signalperiod=5)
        self.prices['fastK'], self.prices['fastD'] = ta.STOCHF(self.prices['High'], self.prices['Low'], self.prices['Close'],
                                                   fastk_period=14, fastd_period=3, fastd_matype=0)
        self.prices['upperband'], self.prices['middleband'], self.prices['lowerband '] = ta.BBANDS(self.prices['Close'],
                                                                                                    timeperiod=30,
                                                                                                   nbdevup=2,
                                                                                                   nbdevdn=2, matype=0)
        # determine the MACD upward or downward
        self.prices['p'] = self.prices['macd'] - self.prices['macd_signal']

    def calculating(self, step: str = 'first') -> None:
        """
        Based On the calculating indicators calculating the first and the other step for making decision
        :param step:
        :return: None
        """
        self.cal_indicators()

        if self.prices['fastK'].values[-1] > 80 and \
                ((self.prices['fastK'].values[-1] - self.prices['fastD'].values[-1]) < 0):
            self.stock = True

        elif self.prices['fastK'].values[-1] < 20 and \
                ((self.prices['fastK'].values[-1] - self.prices['fastD'].values[-1]) > 0):
            self.stock = False

        if step != 'first':
            if self.prices['rsi'].values[-1] < 50 and self.stock and self.prices['p'].values[-1] < 0 and self.stock:
                self.macd = True
                self.rsi = True

            if self.prices['rsi'].values[-1] > 50 and self.stock and self.prices['p'].values[-1] > 0 and not self.stock:
                self.macd = False
                self.rsi = False

    def signal(self) -> str:
        """
        for anyone who just want the signal.
        instead of call the start func should use this func.
        :return: Signal for Buy and Sell : 'Sell' or 'Buy'
        """
        self.reset()
        self.start()
        return self.prime_signal


    def reset(self) -> None:
        self.prime_signal = None
        self.rsi = None
        self.macd = None
        self.stock = None

    def sl_tp(self) -> None:
        """
         close the order if price reach the stop loss price or take profit order
        """
        inside = True
        while inside:
            self.cal_indicators()
            pull = self.client.get_ticker(f'{self.symbol}T')
            price = pull['price']
            if (round(self.prices['lowerband'], 1) - 50) <= price <= (round(self.prices['lowerband'], 1) + 50):
                # close order
                inside = False

            if (round(self.prices['upperband'], 1) - 50) <= price <= (round(self.prices['upperband'], 1) + 50):
                # close order
                inside = False

        self.reset()

    def decision(self) -> None:
        """
        after calculating it will decision to place buy or sell order
        """
        t = self.stock
        inside = True
        while inside:

            if self.stock:
                self.calculating(step='second')

                if self.macd and self.rsi:
                    if self.auto:
                        self.buy()
                        break
                    else:
                        self.prime_signal = 'Buy'
                        break

            elif not self.stock:
                self.calculating(step='second')

                if not self.macd and not self.rsi:
                    if self.auto:
                        self.sell()
                        break
                    else:
                        self.prime_signal = 'Sell'
                        break

            elif t != self.stock:
                inside = False

                sleep(1)

    def start(self) -> None:
        """
        call this func if you leave auto True.
        """
        while True:
            self.calculating()

            if self.stock is not None:
                self.decision()

            if self.prime_signal is not None:
                break

            sleep(1)

    def buy(self):
        # open order
        self.sl_tp()

    def sell(self):
        # open order
        self.sl_tp()


if __name__ == '__main__':
    a = AutoTrade()
    a.start()
