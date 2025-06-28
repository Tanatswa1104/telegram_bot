from flask import Flask, request
import requests
import json

# === Flask App ===
app = Flask(__name__)

# === Your Telegram Bot Token ===
BOT_TOKEN = "7211541859:AAFCikiNNKXDc79f2FtiQ53SnihYqQudddI"

# === Your Endpoint URL for Telegram to hit (you’ll set this later) ===
WEBHOOK_URL = f"https://your-ngrok-url-here/{BOT_TOKEN}"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def handle_update():
    update = request.get_json()

    if "callback_query" in update:
        query = update["callback_query"]
        data = query["data"]
        chat_id = query["message"]["chat"]["id"]
        message_id = query["message"]["message_id"]

        if data.startswith("confirm_"):
            symbol = data.split("_")[1]
            response_text = f"✅ Trade Confirmed for {symbol}"
            print(f"[CONFIRM] {symbol} confirmed")

        elif data.startswith("reject_"):
            symbol = data.split("_")[1]
            response_text = f"❌ Trade Rejected for {symbol}"
            print(f"[REJECT] {symbol} rejected")

        # Answer the callback so Telegram UI updates
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",
            json={"callback_query_id": query["id"]}
        )

        # Edit original message to reflect the choice
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText",
            json={
                "chat_id": chat_id,
                "message_id": message_id,
                "text": response_text
            }
        )

    return "OK", 200

if __name__ == "main":
    app.run(port=5000)
