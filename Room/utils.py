from django.core.mail import send_mail
from Project_uni.settings import EMAIL_HOST_USER
import yfinance as yf
import talib as ta
import pandas as pd


def send_mail_auth(auth_number: int, email_adrress: str) -> None:
    send_mail(
        'Authentication',
        f'Your Code Is {auth_number}',
        EMAIL_HOST_USER,
        recipient_list=[email_adrress, ],
        fail_silently=False,
    )


def get_stock_details(symbol: str, interval: str, period: str) -> pd.DataFrame:
    btc = yf.Ticker(symbol)
    prices = btc.history(period=period, interval=interval)
    return prices


def calculate_indicators(crypto: type) -> None:
    prices = get_stock_details(crypto.crypto_type, interval='30m', period='10d')
    prices['macd'], prices['macd_signal'], prices['macd_histogram'] = ta.MACD(prices['Close'])
    prices['rsi'] = ta.RSI(prices['Close'], timeperiod=14)
    prices['slowk'], prices['slowd'] = ta.STOCH(prices['High'],
                                                prices['Low'],
                                                prices['Close'],
                                                fastk_period=5,
                                                slowk_period=3,
                                                slowk_matype=0,
                                                slowd_period=3,
                                                slowd_matype=0
                                                )
    histogram = prices['macd_histogram'].values[-3:]
    diff = prices['macd'].values[-1] - prices['macd_signal'].values[-1]
    rsi = prices['rsi'].values[-1]
    hastic = prices['slowk'].values[-1] - prices['slowd'].values[-1]
    calculate = {'histogram': histogram,
                 'diff': diff,
                 'rsi': rsi,
                 'hastic': hastic,
                 }
    print(histogram, diff, hastic, rsi)
    crypto.description = macd_dec(calculate)
    crypto.save()


def macd_dec(indicators_cal: dict) -> str:
    signal_macd = ''
    if -10 < indicators_cal['histogram'][-1] < 10 and indicators_cal['diff'] > 0:

        if indicators_cal['histogram'][-2] < 0 or indicators_cal['histogram'][-3] < 0:
            signal_macd = 'Buy'

        elif indicators_cal['histogram'][-2] > 0 or indicators_cal['histogram'][-3] > 0:
            signal_macd = 'Sell'

    elif -10 < indicators_cal['histogram'][-1] < 10 and indicators_cal['diff'] < 0:

        if indicators_cal['histogram'][-2] < 0 or indicators_cal['histogram'][-3] < 0:
            signal_macd = 'Buy'

        elif indicators_cal['histogram'][-2] > 0 or indicators_cal['histogram'][-3] > 0:
            signal_macd = 'Sell'

    return stock_dec(signal_macd, indicators_cal['rsi'], indicators_cal['hastic'])


def stock_dec(signal_macd: str, rsi: int, hastic: int) -> str:
    signal = 'No Signal'
    if rsi > 70:

        if signal_macd == 'Sell' and hastic < 0:
            signal = 'Sell'

        elif signal_macd == '' and hastic < 0:
            signal = 'maybe Sell'

    elif rsi < 30:
        if signal_macd == 'Sell' and hastic > 0:
            signal = 'Buy'

        elif signal_macd == '' and hastic > 0:
            signal = 'maybe Buy'

    else:
        if signal_macd == 'Buy' and hastic < 0:
            signal = 'maybe Buy'

        elif signal_macd == 'Sell' and hastic > 0:
            signal = 'maybe Sell'

    return description_make(signal)


def description_make(signals: str) -> str:
    description = 'با پردازش داده های 3 اندیکاتور نمی توان نظری قطعی درباره خرید یا فروش داد'
    if signals == 'Buy':
        description = 'می توان این را در نظر گرفت با پردازش داده های 3 اندیکاتور خرید در این لحظه را بهترین گزینه ' \
                      'ممکن دانست'

    elif signals == 'Sell':
        description = 'می توان این را در نظر گرفت با پردازش داده های 3 اندیکاتور فروش در این لحظه را بهترین گزینه ' \
                      'ممکن دانست'

    elif signals == 'maybe Sell':
        description = 'می توان این را در نظر گرفت با پردازش داده های 3 اندیکاتور، فروش در این لحظه را بهترین گزینه ' \
                      'ممکن دانست. باید در نظر گرفت این گزینه در این لحظه بهترین گزینه ممکن نباشد، پس با تامل بیشتر ' \
                      'نسبت به خرید اقدام کنید.'

    elif signals == 'maybe Buy':
        description = 'می توان این را در نظر گرفت با پردازش داده های 3 اندیکاتور، خرید در این لحظه را بهترین گزینه ' \
                      'ممکن دانست. باید در نظر گرفت این گزینه در این لحظه بهترین گزینه ممکن نباشد، پس با تامل بیشتر ' \
                      'نسبت به خرید اقدام کنید.'

    return description
