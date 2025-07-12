# save_scalers.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

# Load sample data
df_gbpjpy = pd.read_csv("GBPJPY_sample.csv")
df_xauusd = pd.read_csv("XAUUSD_sample.csv")

# Ensure all columns are lowercase
df_gbpjpy.columns = df_gbpjpy.columns.str.lower()
df_xauusd.columns = df_xauusd.columns.str.lower()

# Rename 'tick_volume' to 'volume'
df_gbpjpy.rename(columns={'tick_volume': 'volume'}, inplace=True)
df_xauusd.rename(columns={'tick_volume': 'volume'}, inplace=True)

# Keep only required columns
FEATURE_COLUMNS = ['open', 'high', 'low', 'close', 'volume']
df_gbpjpy = df_gbpjpy[FEATURE_COLUMNS]
df_xauusd = df_xauusd[FEATURE_COLUMNS]

# Create and save scalers
scaler_gbpjpy = StandardScaler()
scaler_gbpjpy.fit(df_gbpjpy)
joblib.dump(scaler_gbpjpy, "scaler_gbpjpy.save")

scaler_xauusd = StandardScaler()
scaler_xauusd.fit(df_xauusd)
joblib.dump(scaler_xauusd, "scaler_xauusd.save")

print("✅ Scalers saved successfully.")