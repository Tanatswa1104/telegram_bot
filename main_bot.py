import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import time

import requests

TELEGRAM_TOKEN = '7211541859:AAFCikiNNKXDc79f2FtiQ53SnihYqQudddI'
CHAT_ID = '7682710795'

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        print("✅ Telegram alert sent.")
    except Exception as e:
        print("❌ Telegram failed:", e)

# Load AI models
model_gbp = load_model("models/model_gbpjpy.h5")
model_xau = load_model("models/model_xauusd.h5")

# Connect to MetaTrader 5
if not mt5.initialize():
    print("MT5 initialization failed")
    mt5.shutdown()
    quit()

symbols = ["GBPJPYm", "XAUUSDm"]

# Predict direction using AI
def predict_direction(df, model, scaler, sequence_length=10):
    df = df.copy()

    df['candle_body'] = df['close'] - df['open']
    df['upper_wick'] = df['high'] - df[['close', 'open']].max(axis=1)
    df['lower_wick'] = df[['close', 'open']].min(axis=1) - df['low']
    df['pct_change'] = df['close'].pct_change().fillna(0)

    df = df[-sequence_length:]

    features = ['open', 'high', 'low', 'close', 'tick_volume',
                'candle_body', 'upper_wick', 'lower_wick', 'pct_change']

    for col in features:
        if col not in df.columns:
            df[col] = 0.0

    scaled = scaler.fit_transform(df[features])  # shape (10, 9)
    X_input = np.expand_dims(scaled, axis=0)     # shape (1, 10, 9)

    prediction = model.predict(X_input, verbose=0)[0][0]
    direction = "BUY" if prediction > 0.5 else "SELL"
    confidence = round(float(prediction), 4)

    return direction, confidence

# Calculate SL and TP based on direction and point

def calculate_sl_tp(symbol, direction, point, entry_price):
    pip_value = 10 * point  # 10 pips
    if direction == "BUY":
        sl = round(entry_price - (1.5 * pip_value), 3)
        tp = round(entry_price + (3.0 * pip_value), 3)
    else:
        sl = round(entry_price + (1.5 * pip_value), 3)
        tp = round(entry_price - (3.0 * pip_value), 3)
    return sl, tp

# Main loop
while True:
    for symbol in symbols:
        # Get last 100 candles
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 100)
        if rates is None or len(rates) < 20:
            print(f"No data for {symbol}")
            continue

        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')

        # Predict with the correct model
        if symbol == "GBPJPYm":
            direction, confidence = predict_direction(df, model_gbp, MinMaxScaler())
        elif symbol == "XAUUSDm":
            direction, confidence = predict_direction(df, model_xau, MinMaxScaler())
        else:
            continue

        # Calculate SL, TP, Entry
        symbol_info = mt5.symbol_info(symbol)
        point = symbol_info.point
        tick = mt5.symbol_info_tick(symbol)
        price = tick.ask if direction == "BUY" else tick.bid
        sl, tp = calculate_sl_tp(symbol, direction, point, price)

        # Only send high-confidence trades
        if confidence >= 0.55:
            message = f"""
📡 AI Forex Signal
Symbol: {symbol}
🧠 Prediction: {direction}
🎯 Confidence: {confidence}

📍 Entry: {price}
🛡️ SL: {sl}
🎯 TP: {tp}
"""
            send_telegram_alert(message)

    # Wait before next check
    time.sleep(30)

# Shutdown MT5
mt5.shutdown()