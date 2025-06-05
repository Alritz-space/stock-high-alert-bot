import json
import yfinance as yf
import smtplib
from email.mime.text import MIMEText

def load_stock_data(path='stocks.json'):
    with open(path, 'r') as f:
        return json.load(f)["stocks"]

def check_prices(stocks):
    hit_stocks = []
    for stock in stocks:
        symbol = stock["symbol"]
        ath = stock["all_time_high"]
        try:
            ticker = yf.Ticker(symbol)
            current_price = ticker.history(period="1d")["Close"].iloc[-1]
            if current_price >= ath:
                hit_stocks.append(f"{symbol} hit its ATH! ₹{current_price:.2f} (ATH: ₹{ath})")
        except Exception as e:
            hit_stocks.append(f"Error checking {symbol}: {str(e)}")
    return hit_stocks

def send_email_alert(messages, sender_email, receiver_email, app_password):
    if not messages:
        return

    subject = "🚨 Stock Alert: ATH Reached!"
    body = "\n".join(messages)
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

def main():
    stocks = load_stock_data()
    messages = check_prices(stocks)
    
    # Get secrets from GitHub environment variables
    sender_email = os.getenv("EMAIL_FROM")
    receiver_email = os.getenv("EMAIL_TO")
    app_password = os.getenv("EMAIL_PASS")

    send_email_alert(messages, sender_email, receiver_email, app_password)
    
    for msg in messages:
        print(msg)

if __name__ == "__main__":
    import os
    main()

