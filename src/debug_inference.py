import pandas as pd
import numpy as np
import os
import sys
# sys.path.append(os.path.join(os.path.dirname(__file__))) 
from inference import SepsisPredictor

def test():
    # Model is in the same directory
    model_path = os.path.join(os.path.dirname(__file__), 'sepsis_xgboost.pkl')
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

    # Test 3: With Context + History (Deterioration)
    # Previous: MAP 80, HR 100
    # Current: MAP 50, HR 130
    history = [
        {"HR": 100, "MAP": 80, "SBP": 110, "O2Sat": 98, "Temp": 38.0, "Resp": 20},
        {"HR": 110, "MAP": 70, "SBP": 90, "O2Sat": 95, "Temp": 38.5, "Resp": 24}
    ]
    prob_3 = predictor.predict(data_2, history=history)
    print(f"Test 3 (Context + History): Prob={prob_3:.4f}")

    # Test 4: Athlete (Stable) with Context
    # Original Data: {"HR": 55, "MAP": 83, "SBP": 110, "O2Sat": 99, "Temp": 36.6, "Resp": 14}
    data_4 = {"HR": 55, "MAP": 83, "SBP": 110, "O2Sat": 99, "Temp": 36.6, "Resp": 14}
    data_4['Age'] = 25 # Young
    data_4['Gender'] = 1
    data_4['ICULOS'] = 10 
    prob_4 = predictor.predict(data_4)
    print(f"Test 4 (Athlete + Context): Prob={prob_4:.4f}")

    # Test 5: Elderly Stable with Context
    data_5 = data_4.copy()
    data_5['Age'] = 80 # Elderly but stable vitals
    prob_5 = predictor.predict(data_5)
    print(f"Test 5 (Elderly Stable + Context): Prob={prob_5:.4f}")

if __name__ == "__main__":
    test()
