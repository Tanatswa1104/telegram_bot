import MetaTrader5 as mt5

# Connect to MT5
if not mt5.initialize():
    print("❌ Failed to initialize MT5:", mt5.last_error())
    quit()

# Get and print all symbols
symbols = mt5.symbols_get()
print("✅ Symbols available in Market Watch:\n")
for s in symbols:
    print(s.name)

mt5.shutdown()