import pandas as pd
import numpy as np
import os
import sys
from inference import SepsisPredictor

def test():
    model_path = os.path.join(os.path.dirname(__file__), 'src/sepsis_xgboost.pkl')
    try:
        predictor = SepsisPredictor(model_path)
    except Exception as e:
        print(f"Failed to load model: {e}")
        return

    # Critical Case: Septic Shock (Scenario 11)
    # Original Data: {"HR": 130, "MAP": 50, "SBP": 70, "O2Sat": 90, "Temp": 39.5, "Resp": 30}
    
    # Test 1: Baseline (as is)
    data_1 = {"HR": 130, "MAP": 50, "SBP": 70, "O2Sat": 90, "Temp": 39.5, "Resp": 30}
    prob_1 = predictor.predict(data_1)
    print(f"Test 1 (Raw): Prob={prob_1:.4f}")

    # Test 2: With Context (Age, ICULOS)
    data_2 = data_1.copy()
    data_2['Age'] = 65
    data_2['Gender'] = 1
    data_2['ICULOS'] = 50
    data_2['HospAdmTime'] = -50
    prob_2 = predictor.predict(data_2)
    print(f"Test 2 (With Context): Prob={prob_2:.4f}")

if __name__ == "__main__":
    test()
