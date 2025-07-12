from telegram_bot import send_trade_alert

# Simulated trade signal data
symbol = "XAUUSD"
direction = "Sell"
entry_price = 2330.75
stop_loss = 2340.00
take_profit = 2310.50

# Send test alert
send_trade_alert(symbol, direction, entry_price, stop_loss, take_profit) 