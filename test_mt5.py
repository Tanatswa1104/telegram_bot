import MetaTrader5 as mt5

# Initialize MetaTrader 5 connection
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
else:
    print("Connected to MetaTrader 5")
    account_info = mt5.account_info()
    if account_info is not None:
        print("Login:", account_info.login)
        print("Balance:", account_info.balance)
    else:
        print("Failed to retrieve account info")