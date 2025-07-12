import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("XAUUSD_sample.csv")

# Use only the 'close' column
data = df['close'].values.reshape(-1, 1)

# Normalize
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# Create sequences
sequence_length = 20
X, y = [], []

for i in range(len(data_scaled) - sequence_length - 1):
    X.append(data_scaled[i:i+sequence_length])
    # Label: 1 if next close is higher than current, else 0
    y.append(1 if data_scaled[i+sequence_length] > data_scaled[i+sequence_length-1] else 0)

X = np.array(X)
y = np.array(y)

# Build LSTM model
model = Sequential()
model.add(LSTM(64, input_shape=(X.shape[1], X.shape[2])))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Train
history = model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2)

# Save model
model.save("model_xauusd.h5")
print("✅ Model saved as model_xauusd.h5")

# Optional: Plot accuracy
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Val Accuracy')
plt.legend()
plt.show()