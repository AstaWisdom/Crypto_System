from tkinter import *
import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from time import sleep
from kucoin.client import Client
from autotrade import AutoTrade
import talib as ta
import mplfinance as mpf
import yfinance as yf
from threading import Thread

api_key = '61a1f8454e0ec70001f5adbf'
api_secret = 'd7d36a40-4b6a-4f68-98e2-ae946c2ca303'
api_pass = 'Qwertyui12345'
all_threads = []

class Application:
    def __init__(self, root):
        # CLient for Kucoin Api
        self.client = Client(api_key, api_secret, api_pass)
        # Auto Trade
        self.trade_auto_app = AutoTrade(client=self.client)
        # Variables
        self.coin_selection = IntVar()
        self.token = None
        self.coin_selection.set(1)
        self.var_radio = IntVar()
        self.interval_chart = StringVar()
        self.interval_chart.set('30m')
        self.loged_in = False
        self.email_user = None
        self.client_oid = None
        self.money_user = None
        # Root Window
        self.window = root
        self.window.resizable(True, True)
        self.window.geometry("1300x900")
        self.window.title("Meta")
        self.window.maxsize(1300, 900)
        # Pop Up Window
        self.log_in = Toplevel(self.window)
        self.trade_window = Toplevel(self.window)
        self.trade_window.protocol("WM_DELETE_WINDOW", self.exit_auto_trade_window)
        self.log_in.protocol("WM_DELETE_WINDOW", self.exit_auto_trade_window)
        self.manual = None
        self.auto = None
        self.trade_window.geometry('600x400')
        self.trade_window.resizable(False, False)
        # Description for Indicators
        self.description = 'Should Click on One of the Indicators.'
        # Indicators Frame
        self.candles_frame = Frame(self.window, width=1000, height=700, relief=GROOVE, )
        self.candles_frame.place(x=0, y=0)
        self.macd_indicator = Button(self.candles_frame, text='MACD', relief=GROOVE, command=self.indicators_macd)
        self.ma_indicator = Button(self.candles_frame, text='Moving Average', relief=GROOVE,
                                   command=self.indicator_moving_average,
                                   )
        self.stockhastic_indicator = Button(self.candles_frame, text='Stoch Hastic', relief=GROOVE,
                                            command=self.indicator_stock_hastic,
                                            )
        self.rsi_indicator = Button(self.candles_frame, text='RSI', relief=GROOVE,
                                    command=self.indicator_rsi,
                                    )
        self.macd_indicator.place(x=0, y=675)
        self.ma_indicator.place(x=45, y=675)
        self.stockhastic_indicator.place(x=141, y=675)
        self.rsi_indicator.place(x=215, y=675)
        # Bottom Frame
        self.bottom_frame = Frame(self.window, width=1400, height=200)
        self.bottom_frame.pack(side=BOTTOM)
        self.description_radio = Radiobutton(
            self.bottom_frame,
            variable=self.var_radio,
            value=1,
            indicatoron=False,
            text='Description',
            command=self.footer,
            )
        self.orders = Radiobutton(
            self.bottom_frame,
            variable=self.var_radio,
            value=2,
            indicatoron=False,
            text='Orders',
            command=self.footer,
            )
        self.description_radio.place(x=0, y=175)
        self.orders.place(x=70, y=175)
        # Top Right Frame
        self.btc = Radiobutton(
            self.window,
            text='BitCoin',
            variable=self.coin_selection,
            value=1,
        )
        self.eth = Radiobutton(
            self.window,
            text='Ethereum',
            variable=self.coin_selection,
            value=2,
        )
        self.btc.place(x=1050, y=5)
        self.eth.place(x=1050, y=25)
        self.l_1 = Label(master=self.window, text='Price:')
        self.l_2 = Label(master=self.window, relief=SUNKEN, width=10)
        self.l_3 = Label(master=self.window, text='Buy Price:')
        self.l_4 = Label(master=self.window, relief=SUNKEN, width=10)
        self.l_5 = Label(master=self.window, text='Sell Price:')
        self.l_6 = Label(master=self.window, relief=SUNKEN, width=10)
        self.l_1.place(x=1120, y=85)
        self.l_2.place(x=1100, y=105)
        self.error = Label(self.log_in, fg='red')
        self.buy_button = Button(self.window, text='Buy', command=self._buy, width=10)
        self.sell_button = Button(self.window, text='Sell', command=self._sell, width=10)
        self.buy_button.place(x=1050, y=200)
        self.sell_button.place(x=1150, y=200)
        # For Log In
        self.box_enter1 = None
        self.box_enter2 = None
        self.box_enter3 = None

        # Time Frames for Chart
        # In the Candle Frame
        self.m5 = Radiobutton(
            self.candles_frame,
            variable=self.interval_chart,
            value='5m',
            indicatoron=False,
            text='5m',
            command=self.chart_stock,
        )
        self.m15 = Radiobutton(
            self.candles_frame,
            variable=self.interval_chart,
            value='15m',
            indicatoron=False,
            text='15m',
            command=self.chart_stock,
        )
        self.m30 = Radiobutton(
            self.candles_frame,
            variable=self.interval_chart,
            value='30m',
            indicatoron=False,
            text='30m',
            command=self.chart_stock,
        )
        self.h1 = Radiobutton(
            self.candles_frame,
            variable=self.interval_chart,
            value='1h',
            indicatoron=False,
            text='1h',
            command=self.chart_stock,
        )
        self.m90 = Radiobutton(
            self.candles_frame,
            variable=self.interval_chart,
            value='90m',
            indicatoron=False,
            text='90m',
            command=self.chart_stock,
        )
        self.d1 = Radiobutton(
            self.candles_frame,
            variable=self.interval_chart,
            value='1d',
            indicatoron=False,
            text='1d',
            command=self.chart_stock,
        )
        self.m5.place(x=0, y=0)
        self.m15.place(x=25, y=0)
        self.m30.place(x=55, y=0)
        self.h1.place(x=85, y=0)
        self.m90.place(x=107, y=0)
        self.d1.place(x=138, y=0)

    def get_data_stock(self, interval):
        period = '7d'
        if interval == '1d' or interval == '1wk':
            period = '6mo'
        elif interval == '1mo':
            period = '3y'
        if self.coin_selection.get() == 1:
            btc = yf.Ticker('BTC-USD')
            prices = btc.history(period=period, interval=interval)
            return prices
        elif self.coin_selection.get() == 2:
            btc = yf.Ticker('ETH-USD')
            prices = btc.history(period=period, interval=interval)
            return prices

    def draw_chart(self, interval, addplots):
        fig, axlist = mpf.plot(self.get_data_stock(interval),
                               returnfig=True,
                               figsize=(10, 6),
                               type='candle',
                               style='binance',
                               addplot=addplots,
                               )
        chart = FigureCanvasTkAgg(fig, master=self.candles_frame)
        chart.get_tk_widget().place(y=25, x=0)
        toolbar = NavigationToolbar2Tk(chart, self.candles_frame)
        toolbar.update()
        toolbar.place(x=480, y=660)
        chart.draw()

    def chart_stock(self):

        if self.interval_chart.get() == '5m':
            self.draw_chart(self.interval_chart.get(), [])

        elif self.interval_chart.get() == '15m':
            self.draw_chart(self.interval_chart.get(), [])

        elif self.interval_chart.get() == '30m':
            self.draw_chart(self.interval_chart.get(), [])

        elif self.interval_chart.get() == '1h':
            self.draw_chart(self.interval_chart.get(), [])

        elif self.interval_chart.get() == '90m':
            self.draw_chart(self.interval_chart.get(), [])

        elif self.interval_chart.get() == '1d':
            self.draw_chart(self.interval_chart.get(), [])

    def indicators_macd(self):
        prices = self.get_data_stock(self.interval_chart.get())
        prices['macd'], prices['macd_signal'], prices['macd_histogram'] = ta.MACD(prices['Close'])
        colors = ['g' if v >= 0 else 'r' for v in prices["macd_histogram"]]
        macd_plot = mpf.make_addplot(prices['macd'], panel=1, color='fuchsia', title="MACD")
        macd_plot_hist = mpf.make_addplot(prices['macd_histogram'], type='bar', panel=1, color=colors)
        macd_plot_signal = mpf.make_addplot(prices['macd_signal'], panel=1, color='b')
        plots = [macd_plot, macd_plot_hist, macd_plot_signal]
        self.draw_chart(self.interval_chart.get(), plots)
        self.description = 'This indicator consist of 3 parts Signal line Macd line and Histogram.'\
        'Histogram is the bars that means distance between signal and macd line if histogram is big number means' \
        'two line faraway from each other.'\
        'when the histogram is up means macd line is above signal line, when is down means' \
        'macd line is below signal line.'\
        'signal line is the smooth line ( like moving average ), when macd line cross with signal'\
        'line from below we can say that its a buy signal.'\
        'when macd line cross the signal line from above we can say that its a sell signal. ( signal line is Blue line )'
        self.footer()

    def indicator_rsi(self):
        prices = self.get_data_stock(self.interval_chart.get())
        prices['rsi'] = ta.RSI(prices['Close'], timeperiod=14)
        rsi_plot = mpf.make_addplot(prices['rsi'], panel=1, color='violet')
        self.draw_chart(self.interval_chart.get(), [rsi_plot])
        self.description = 'This Indicator Is a line between 100 and 0 when'\
         'the line is above 70 means the market is overbought that means when line'\
          'crossing 70 for going bottom might be a signal for sell This can be buy Signal when crossing 30 for going up'
        self.footer()

    def indicator_stock_hastic(self):
        prices = self.get_data_stock(self.interval_chart.get())
        prices['slowk'], prices['slowd'] = ta.STOCH(prices['High'],
                                                    prices['Low'],
                                                    prices['Close'],
                                                    fastk_period=5,
                                                    slowk_period=3,
                                                    slowk_matype=0,
                                                    slowd_period=3,
                                                    slowd_matype=0
                                                    )
        plot_slowk = mpf.make_addplot(prices['slowk'], panel=1, color='blue')
        plot_slowd = mpf.make_addplot(prices['slowd'], panel=1, color='red')
        plots = [plot_slowd, plot_slowk]
        self.draw_chart(self.interval_chart.get(), plots)
        self.description = 'This indicator consist of two lines fast line and slow line, when fast line cross slow'\
        'line from above can be a sell signal.'\
        'when fast line cross the slow line from below can be a buy signal.'
        self.footer()

    def indicator_moving_average(self):
        prices = self.get_data_stock(self.interval_chart.get())
        prices['ma'] = ta.EMA(prices['Close'])
        ma_plot = mpf.make_addplot(prices['ma'], color='orange')
        self.draw_chart(self.interval_chart.get(), [ma_plot])
        self.description = 'This indicator is Average of Specific Days of Close prices'
        self.footer()

    def prices(self):
        while True:
            if self.loged_in:
                if self.coin_selection.get() == 1:
                    pull = self.client.get_ticker('BTC-USDT')
                    print(pull)
                    price = pull['price']
                    price_bid = pull['bestBid']
                    price_ask = pull['bestAsk']
                    self.l_4['text'] = price_ask
                    self.l_6['text'] = price_bid
                    self.l_2['text'] = price
                    sleep(1)
                if self.coin_selection.get() == 2:
                    pull = self.client.get_ticker('ETH-USDT')
                    print(pull)
                    price = pull['price']
                    price_bid = pull['bestBid']
                    price_ask = pull['bestAsk']
                    self.l_4['text'] = price_ask
                    self.l_6['text'] = price_bid
                    self.l_2['text'] = price
                    sleep(1)


    def footer(self):
        if self.var_radio.get() == 2:
            self.description = ''
            url = 'http://127.0.0.1:8000/getordersapi/?format=json'
            headers = {'Authorization': 'Token ' + self.token}
            response = requests.get(url=url, headers=headers, timeout=2.5).json()
            for res in response.values():
                for i in res.values():
                    self.description += f"ID: {i['order_id']} \t||\t Amount: {i['oder_amount']}\t||\t" \
                                       f"Type: {i['order_type']} \t||\t Size: {i['order_size']} \n"
            print(self.description)
            desc = Text(self.bottom_frame, height=10.5, width=162)
            desc.place(x=0, y=0)
            desc.insert(END, self.description)
            desc.config(state='disabled')
            self.description = 'Should Click on One of the Indicators.'

        elif self.var_radio.get() == 1:
            desc = Text(self.bottom_frame, height=10.5, width=162)
            desc.place(x=0, y=0)
            desc.insert(END, self.description)
            desc.config(state='disabled')
            self.description = 'Should Click on One of the Indicators.'

    def authentication(self):
        username = self.box_enter1.get()
        password = self.box_enter2.get()
        self.token = self.box_enter3.get()

        if username and password and self.token:
            url = 'http://127.0.0.1:8000/Auth/?format=json'
            data = {'username': username, 'password': password}
            response = requests.post(url=url, data=data, timeout=2.5)
            tok = response.content.decode().split(':')[1].strip('}"')
            if tok == self.token:
                self.loged_in = True
                url = 'http://127.0.0.1:8000/apiuserinfo/?format=json'
                headers = {'Authorization': 'Token ' + tok}
                response = requests.get(url=url, headers=headers)
                self.email_user = response.json()['email']
                self.client_oid = response.json()['clientoid']
                self.money_user = int(response.json()['money'])
                self.log_in.destroy()
                self.log_in.update()
                self.trade()
            else:
                self.error.destroy()
                self.error = Label(self.log_in, fg='red')
                self.error['text'] = 'Please Enter Correct Information'
                self.error.pack()

        else:
            self.error.destroy()
            self.error = Label(self.log_in, fg='red')
            self.error['text'] = 'Please Enter All Information'
            self.error.pack()

    def message(self):
        self.log_in.geometry("400x300")
        self.log_in.title("Log in")
        l1 = Label(self.log_in, text="Enter your username")
        l1.pack()
        self.box_enter1 = Entry(master=self.log_in)
        self.box_enter1.pack()
        l2 = Label(self.log_in, text="Enter your Password")
        l2.pack()
        self.box_enter2 = Entry(master=self.log_in, show='*')
        self.box_enter2.pack()
        l3 = Label(self.log_in, text="Enter your Token")
        l3.pack()
        self.box_enter3 = Entry(master=self.log_in)
        self.box_enter3.pack()
        b1 = Button(self.log_in, text="Log In", command=self.authentication)
        b1.pack()

    def trade(self):
        self.trade_window.deiconify()
        self.btc = Radiobutton(
            self.trade_window,
            text='BitCoin',
            variable=self.coin_selection,
            value=1,
        )
        self.eth = Radiobutton(
            self.trade_window,
            text='Ethereum',
            variable=self.coin_selection,
            value=2,
        )
        self.auto = Button(self.trade_window, text='Auto Trade', relief=GROOVE, command=self.auto_trade)
        self.manual = Button(self.trade_window, text='Manualy Trade' , relief=GROOVE, command=self.manualy)
        self.btc.pack()
        self.eth.pack()
        self.auto.pack()
        self.manual.pack()

    def manualy(self):
        self.trade_window.destroy()
        self.trade_window.update()
        self.window.deiconify()

    def auto_trade(self):
        self.l_1 = Label(master=self.trade_window, text='Price:')
        self.l_2 = Label(master=self.trade_window, relief=SUNKEN, width=10)
        self.l_3 = Label(master=self.trade_window, text='Buy Price:')
        self.l_4 = Label(master=self.trade_window, relief=SUNKEN, width=10)
        self.l_5 = Label(master=self.trade_window, text='Sell Price:')
        self.l_6 = Label(master=self.trade_window, relief=SUNKEN, width=10)
        self.btc.destroy()
        self.eth.destroy()
        self.auto.destroy()
        self.manual.destroy()
        self.l_1.pack()
        self.l_2.pack()
        self.l_3.pack()
        self.l_4.pack()
        self.l_5.pack()
        self.l_6.pack()

        if self.coin_selection.get() == 2:
            self.trade_auto_app.symbol = 'ETH-USD'

        t2 = Thread(target=self.trade_auto_app.start)
        t2.setDaemon(True)
        all_threads.append(t2)
        t2.start()

    def exit_auto_trade_window(self):
        self.log_in.destroy()
        self.trade_window.destroy()
        self.window.destroy()

    def _buy(self):
        pass

    def _sell(self):
        pass

    def start(self):
        self.window.withdraw()
        self.trade_window.withdraw()
        self.message()
        self.chart_stock()
        t1 = Thread(target=self.prices)
        t1.setDaemon(True)
        all_threads.append(t1)
        t1.start()


master = Tk()
window = Application(master)
window.start()
master.mainloop()
for t in all_threads:
    t.join(timeout=1)

