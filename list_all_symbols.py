import MetaTrader5 as mt5

mt5.initialize()

symbols = mt5.symbols_get()
print(f"Total symbols found: {len(symbols)}")

for sym in symbols:
    if "GBPJPY" in sym.name or "XAUUSD" in sym.name:
        print(sym.name)

mt5.shutdown()