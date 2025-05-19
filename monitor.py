import yfinance as yf
import schedule
import time
import json
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)["stocks"]

def send_email_alert(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("GMAIL_USER")
    msg["To"] = os.getenv("TO_EMAIL")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_PASS"))
        smtp.send_message(msg)

def monitor():
    stocks = load_config()
    for symbol in stocks:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="max")
            current_price = hist["Close"][-1]
            all_time_high = hist["Close"].max()

            if current_price >= all_time_high:
                message = f"{symbol} hit a new all-time high: ${current_price:.2f}!"
                print(message)
                send_email_alert("📈 Stock Alert", message)
        except Exception as e:
            print(f"Error with {symbol}: {e}")

# Schedule: run every hour
schedule.every(1).hours.do(monitor)

print("✅ Stock alert bot started. Waiting for next check...")
while True:
    schedule.run_pending()
    time.sleep(60)
