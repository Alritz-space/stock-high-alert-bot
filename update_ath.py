import yfinance as yf
import json
import time

def get_ath(symbol):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="max")
        if hist.empty:
            return None
        return round(hist["Close"].max(), 2)
    except Exception as e:
        print(f"[ERROR] {symbol}: {e}")
        return None

def update_ath_file(filepath="stocks.json"):
    with open(filepath, "r") as f:
        data = json.load(f)

    updated = []
    for stock in data["stocks"]:
        symbol = stock["symbol"]
        ath = get_ath(symbol)
        if ath:
            stock["all_time_high"] = ath
            print(f"{symbol}: ATH updated to ₹{ath}")
        else:
            print(f"{symbol}: No ATH found.")
        updated.append(stock)
        time.sleep(1)  # avoid getting rate-limited

    with open(filepath, "w") as f:
        json.dump({"stocks": updated}, f, indent=2)

if __name__ == "__main__":
    update_ath_file()
