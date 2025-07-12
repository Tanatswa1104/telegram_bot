from flask import Flask, request
import requests

app = Flask(__name__)

# === CONFIG ===
BOT_TOKEN = '7211541859:AAFCikiNNKXDc79f2FtiQ53SnihYqQudddI'
CHAT_ID = '7682710795'
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'


# === SEND MESSAGE WITH BUTTONS ===
def send_trade_signal(symbol, direction, confidence, entry, sl, tp):
    message = f"""
📡 AI Forex Signal
Symbol: {symbol}
🧠 Prediction: {direction}
🎯 Confidence: {confidence}

📍 Entry: {entry}
🛡️ SL: {sl}
🎯 TP: {tp}
"""

    keyboard = {
        "inline_keyboard": [[
            {"text": "✅ Confirm", "callback_data": f"confirm_{symbol}"},
            {"text": "❌ Reject", "callback_data": f"reject_{symbol}"}
        ]]
    }

    requests.post(f"{BASE_URL}/sendMessage", json={
        "chat_id": CHAT_ID,
        "text": message,
        "reply_markup": keyboard
    })


# === LISTEN FOR BUTTON PRESSES ===
@app.route('/', methods=["POST"])
def webhook():
    data = request.get_json()

    if 'callback_query' in data:
        chat_id = data['callback_query']['message']['chat']['id']
        query_id = data['callback_query']['id']
        user_response = data['callback_query']['data']

        if user_response.startswith("confirm_"):
            symbol = user_response.split("_")[1]
            reply = f"✅ Trade confirmed for {symbol}!"
        else:
            symbol = user_response.split("_")[1]
            reply = f"❌ Trade rejected for {symbol}."

        # Send response back to Telegram
        requests.post(f"{BASE_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": reply
        })

        # Acknowledge button click
        requests.post(f"{BASE_URL}/answerCallbackQuery", json={
            "callback_query_id": query_id
        })

    return "ok"


# === TEST SEND ===
if __name__ == '__main__':
    # Optional test signal
    send_trade_signal("XAUUSDm", "BUY", 0.6834, 3312.219, 3312.137, 3312.182)
    app.run(host="0.0.0.0", port=5000)