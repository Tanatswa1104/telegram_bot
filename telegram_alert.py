import requests

BOT_TOKEN = "7211541859:AAFCikiNNKXDc79f2FtiQ53SnihYqQudddI"
CHAT_ID = "7682710795"  # your Telegram chat ID

def send_telegram_alert(symbol, direction, entry_price, sl, tp, confidence):
    message = f"""
📡 *{symbol}* Signal: *{direction}*
🎯 Entry: {entry_price}
🛑 SL: {sl}
🎯 TP: {tp}
📊 Confidence: {confidence:.2f}
"""
    # send message to Telegram (already working)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)