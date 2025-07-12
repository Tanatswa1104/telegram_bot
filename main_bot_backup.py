import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import pytz
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import requests
import time

# === 1. Telegram Settings ===
BOT_TOKEN = "7211541859:AAFCikiNNKXDc79f2FtiQ53SnihYqQudddI"
CHAT_ID = "7682710795"

# === 2. Symbol & Model Mapping ===
symbols_models = {
    "GBPJPYm": "model_gbpjpy.h5",
    "XAUUSDm": "model_xauusd.h5"
}

def send_telegram_alert(symbol, signal, confidence):
    msg = f"📡 *AI Signal Detected*\n\n*Symbol:* {symbol}\n*Signal:* {signal}\n*Confidence:* {confidence:.2f}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown",
        "reply_markup": {
            "inline_keyboard": [[
                {"text": "✅ Confirm", "callback_data": f"confirm_{symbol}"},
                {"text": "❌ Reject", "callback_data": f"reject_{symbol}"}
            ]]
        }
    }
    try:
        requests.post(url, json=data)
        print(f"📩 Alert sent for {symbol}: {signal}")
    except Exception as e:
        print(f"❌ Failed to send Telegram alert: {e}")

def check_symbols():
    if not mt5.initialize():
        print("❌ MT5 initialization failed:", mt5.last_error())
        return
    print(f"✅ Connected to MetaTrader 5 at {datetime.now()}")

    for symbol, model_path in symbols_models.items():
        print(f"\n🔍 Checking {symbol}...")

        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 21)
        if rates is None or len(rates) < 21:
            print(f"❌ Not enough data for {symbol}")
            continue

        df = pd.DataFrame(rates)
        close_prices = df['close'].values.reshape(-1, 1)

        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(close_prices)
        X = np.array([data_scaled[-21:-1]])  # last 20 candles

        model = load_model(model_path)
        prediction = model.predict(X)
        confidence = prediction[0][0]

        signal = "Buy" if confidence > 0.6 else "Sell" if confidence < 0.4 else "No Trade"
        print(f"🧠 {symbol} Prediction: {confidence:.4f} → Signal: {signal}")

        if signal != "No Trade":
            send_telegram_alert(symbol, signal, confidence)

    mt5.shutdown()

if __name__ == "__main__":
    while True:
        check_symbols()
        print("\n⏳ Waiting 5 minutes before next check...\n")
        time.sleep(5 * 60)  # Sleep for 5 minutes (300 seconds