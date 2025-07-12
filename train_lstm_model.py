import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Load CSVs
gbpjpy = pd.read_csv("GBPJPY_sample.csv")
xauusd = pd.read_csv("XAUUSD_sample.csv")

# Preprocessing function
def preprocess(df):
    df['time'] = pd.to_datetime(df['time'])
    df['candle_body'] = df['close'] - df['open']
    df['upper_wick'] = df['high'] - df[['close', 'open']].max(axis=1)
    df['lower_wick'] = df[['close', 'open']].min(axis=1) - df['low']
    df['direction'] = np.where(df['close'] > df['open'], 1, 0)
    df['pct_change'] = df['close'].pct_change().fillna(0)

    scaler = MinMaxScaler()
    features = ['open', 'high', 'low', 'close', 'tick_volume', 'candle_body', 'upper_wick', 'lower_wick', 'pct_change']
    df[features] = scaler.fit_transform(df[features])
    return df

# Create sequences
def create_sequences(df, seq_len=10):
    features = ['open', 'high', 'low', 'close', 'tick_volume', 'candle_body', 'upper_wick', 'lower_wick', 'pct_change']
    X, y = [], []
    for i in range(len(df) - seq_len):
        X.append(df[features].iloc[i:i+seq_len].values)
        y.append(df['direction'].iloc[i+seq_len])
    return np.array(X), np.array(y)

# Process data
gbpjpy = preprocess(gbpjpy)
xauusd = preprocess(xauusd)

# Sequences
X_gbp, y_gbp = create_sequences(gbpjpy)
X_xau, y_xau = create_sequences(xauusd)

# Split
X_train_gbp, X_test_gbp, y_train_gbp, y_test_gbp = train_test_split(X_gbp, y_gbp, test_size=0.2, random_state=42)
X_train_xau, X_test_xau, y_train_xau, y_test_xau = train_test_split(X_xau, y_xau, test_size=0.2, random_state=42)

# Build model
def build_model(input_shape):
    model = Sequential([
        LSTM(64, input_shape=input_shape),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Train GBPJPY model
model_gbp = build_model(X_train_gbp.shape[1:])
model_gbp.fit(X_train_gbp, y_train_gbp, epochs=30, batch_size=8, validation_split=0.2)

# Train XAUUSD model
model_xau = build_model(X_train_xau.shape[1:])
model_xau.fit(X_train_xau, y_train_xau, epochs=30, batch_size=8, validation_split=0.2)

# Evaluate
gbp_acc = model_gbp.evaluate(X_test_gbp, y_test_gbp)
xau_acc = model_xau.evaluate(X_test_xau, y_test_xau)

print(f"✅ GBPJPY Accuracy: {gbp_acc[1]*100:.2f}%")
print(f"✅ XAUUSD Accuracy: {xau_acc[1]*100:.2f}%")

# Optional: Save models
model_gbp.save("model_gbpjpy.h5")
model_xau.save("model_xauusd.h5")
