import requests

TELEGRAM_BOT_TOKEN = '7211541859:AAFCikiNNKXDc79f2FtiQ53SnihYqQudddI'
TELEGRAM_CHAT_ID = '7682710795'

def send_trade_alert(symbol, entry, sl, tp, confluences):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessages"
    message = (
        f"*AI Trade Signal*\n"
        f"Symbol: {symbol}\n"
        f"Entry: {entry}\n"
        f"Stop Loss: {sl}\n"
        f"Take Profit: {tp}\n"
        f"Confluences: {confluences}\n"
        f"Lot Size: 0.01\n"
        f"[Confirm] | [Reject]"
    )
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=payload)