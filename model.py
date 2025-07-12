import numpy as np
import joblib
from tensorflow.keras.models import load_model

def load_model_and_scaler(symbol):
    if "XAUUSD" in symbol:
        model = load_model("model_xauusd.h5")
        scaler = joblib.load("scaler_xauusd.save")
    else:
        model = load_model("model_gbpjpy.h5")
        scaler = joblib.load("scaler_gbpjpy.save")
    return model, scaler

def predict_signal(model, scaler, features):
    features_scaled = scaler.transform([features])
    prediction = model.predict(features_scaled)[0][0]
    signal = "Buy" if prediction > 0.55 else "Sell" if prediction < 0.45 else "No Trade"
    return prediction, signal