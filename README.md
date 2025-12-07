🚀 Crypto Trading & Analysis System (Python + Django + Tkinter)

A full crypto trading system with live price fetching, technical indicators, and automated trading decision logic.
Developed as an end-to-end academic project demonstrating algorithmic trading, market indicators, and decision-making automation.

✨ Features

Live prices using KuCoin & Yahoo Finance

Technical indicators using TA-Lib

MACD, RSI, Stochastic, Bollinger Bands

Automated trade signal generation

Django backend + REST API

Desktop GUI (Tkinter)

Buy/Sell logic simulation

User authentication via Django

Indicator-based decision engine

🧠 Core Idea

This project combines multiple indicators to generate buy/sell signals:

MACD trend

RSI overbought/oversold

Stochastic momentum

Bollinger channel positions

Then the system decides:

Buy

Sell

or Hold (no signal)

This demonstrates algorithmic thinking and technical-analysis-based market strategies.

🧩 Architecture Overview
/django_backend
   models.py
   views.py
   indicators
   api routes

/desktop_app
   tkinter UI
   live charts (mplfinance)
   trading logic

📊 Indicators Used

MACD (trend direction)

RSI (market condition)

Stochastic (momentum)

Bollinger Bands (volatility)

All indicators are calculated using TA-Lib and updated live based on selected symbol and timeframe.

🖥 Desktop App (Tkinter)

Real-time chart visualization

User authentication

Price display (bid/ask)

Indicator buttons

Auto-trade mode

Manual trading mode

Live candle chart

🔌 Backend (Django)

User registration & token auth

API endpoints

Orders storage

Indicator description returned by API

Email confirmation (optional)

🧪 Trading Logic
Pseudocode
if MACD crosses signal upward and RSI < 50 and Stochastic positive:
        BUY
elif MACD crosses downward and RSI > 50 and Stochastic negative:
        SELL
else:
        NO SIGNAL


This demonstrates how multiple indicators together can produce a trading decision.

⚠️ Disclaimer

This system is developed for educational and research purposes only.
It is not intended for real-world trading without risk evaluation.

💡 What this shows in a resume

Python desktop UI

Django backend

REST API

Data analysis

Algorithmic decision-making

Technical indicators

API integration (KuCoin)

Real-time data handling

Trading system design

👤 Author

Developed as a university project integrating software engineering and financial algorithm design
