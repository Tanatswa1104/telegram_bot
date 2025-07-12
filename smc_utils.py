# smc_utils.py

import pandas as pd

# === Step 1: Detect Swing Highs and Lows ===
def detect_swings(df, left=3, right=3):
    df['swing_high'] = False
    df['swing_low'] = False

    for i in range(left, len(df) - right):
        is_high = all(df['high'][i] > df['high'][i - j] and df['high'][i] > df['high'][i + j] for j in range(1, left + 1))
        is_low = all(df['low'][i] < df['low'][i - j] and df['low'][i] < df['low'][i + j] for j in range(1, left + 1))

        if is_high:
            df.at[i, 'swing_high'] = True
        if is_low:
            df.at[i, 'swing_low'] = True

    return df

# === Step 2: Detect BOS (Break of Structure) ===
def detect_bos(df):
    df['bos'] = False
    last_high = None
    last_low = None

    for i in range(len(df)):
        if df['swing_high'][i]:
            last_high = df['high'][i]
        if df['swing_low'][i]:
            last_low = df['low'][i]

        if last_high and df['close'][i] > last_high:
            df.at[i, 'bos'] = True
            last_high = None  # reset
        elif last_low and df['close'][i] < last_low:
            df.at[i, 'bos'] = True
            last_low = None

    return df

# === Step 3: Filter based on SMC structure ===
def smc_filter(df):
    df = detect_swings(df)
    df = detect_bos(df)

    # Confirm if BOS just occurred
    if df['bos'].iloc[-1]:
        return True
    return False