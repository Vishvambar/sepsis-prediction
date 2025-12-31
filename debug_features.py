import joblib
import os

try:
    features = joblib.load('src/sepsis_xgboost.pkl.features')
    print("Expected Features:", features)
except Exception as e:
    print(e)
