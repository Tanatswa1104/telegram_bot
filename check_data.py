import MetaTrader5 as mt5
import pandas as pd

mt5.initialize()

symbols = ["GBPJPY", "XAUUSD"]  # Or try adding 'm', like 'GBPJPYm'

for symbol in symbols:
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 10)
    print(f"\n{symbol} →", "✅ Found" if rates is not None and len(rates) > 0 else "❌ Not Found")

    if rates is not None and len(rates) > 0:
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        print(df[['time', 'open', 'close']].tail())

mt5.shutdown()