# Crypto Trading & Analysis System (Python + Django + Tkinter)

A complete crypto trading and analysis system using Python, Django REST API, TA-Lib technical indicators, and a desktop UI.  
This project was developed as a university thesis combining algorithmic decision-making, financial indicators, and software engineering.

---

## ✨ Key Features

- Live price fetching (KuCoin / Yahoo Finance)
- Technical indicators:
  - MACD
  - RSI
  - Stochastic
  - Bollinger Bands
- Automated trading logic (Buy / Sell decisions)
- Django backend API (user, crypto, orders)
- Token authentication (Django REST Token)
- Tkinter desktop interface
- Real-time charts (mplfinance)
- Auto-trade mode + manual trade mode

---

## 🧠 Algorithmic Idea

Instead of a single indicator, the system evaluates market conditions based on multiple indicators:

- MACD direction
- RSI thresholds
- Stochastic cross signals
- Bollinger upper/lower bands

This produces a combined signal:



Buy
Sell
maybe Buy
maybe Sell
No Signal


This demonstrates how multiple signals can be merged to make decisions.

---

## 🧩 Architecture



/crypto_backend (Django)
├── models.py
├── views.py
├── indicators/
├── api routes
└── authentication

/desktop_app (Tkinter)
├── realtime charts
├── auto-trade logic
├── live prices
└── user authentication


Backend generates indicator analysis; Tkinter app visualizes and performs trading actions.

---

## 📊 Technical Indicators

Indicator packages:
- TA-Lib
- yfinance
- mplfinance

Indicators processed:
- MACD
- RSI
- Stochastic Oscillator
- Bollinger Bands

---

## 🖥 Desktop Application

- Login screen
- Real-time price display (bid/ask)
- Candle charts
- Indicator visualization
- Auto-trade enabling
- Manual Buy/Sell
- Multiple timeframes (5m, 15m, 30m, 1h, 1day)

---

## 🔌 Backend (Django)

- User registration
- Token authentication
- Orders API
- Indicator results stored in DB
- Email confirmation logic

Example API response:
```json
{
  "email": "user@example.com",
  "clientoid": "123456",
  "money": 500
}

🚀 Run Locally
Backend
cd django_backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Desktop app
cd desktop_app
python main.py

⚠️ Important

This project was developed for educational and research purposes.
It is not intended for real-world crypto trading without risk evaluation and financial supervision.

🎯 What this project demonstrates (good for resume)

Python OOP

Desktop UI (Tkinter)

Django REST Framework

Real-time data

Algorithmic trading logic

Multiple indicators

Decision making

API integration

Chart visualization

Auto-trade logic

Software architecture skills

Perfect example of combining software engineering with financial algorithms.

🔐 Security Notes

Do NOT store real API keys in source code.
Use environment variables and .env for credentials.
Remove production database before publishing.

👨‍💻 Author

Created as a university project integrating software design, data processing, and financial market analysis.


---
