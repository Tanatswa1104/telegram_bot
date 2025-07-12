import pandas as pd
import random
from datetime import datetime, timedelta

# Create sample OHLC data
def generate_data(symbol="GBPJPY", num_bars=100):
    start = datetime.now() - timedelta(minutes=num_bars * 5)
    data = []
    price = 200  # starting price

    for i in range(num_bars):
        open_price = price + random.uniform(-0.5, 0.5)
        high = open_price + random.uniform(0.1, 0.5)
        low = open_price - random.uniform(0.1, 0.5)
        close = low + random.uniform(0, (high - low))
        volume = random.randint(100, 500)

        data.append([
            start + timedelta(minutes=i * 5),
            open_price, high, low, close, volume
        ])
        price = close  # update price for next bar

    df = pd.DataFrame(data, columns=["time", "open", "high", "low", "close", "tick_volume"])
    df.to_csv(f"{symbol}_sample.csv", index=False)
    print(f"Generated sample data saved to {symbol}_sample.csv")

generate_data("GBPJPY")
generate_data("XAUUSD")