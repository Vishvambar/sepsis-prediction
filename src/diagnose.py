
import argparse
import os
import sys

# Ensure src is in path
sys.path.append(os.path.dirname(__file__))

from inference import SepsisPredictor
from clinical_rules import apply_clinical_rules

def get_risk_label(prob):
    if prob >= 0.22: return "CRITICAL"
    if prob >= 0.08: return "WARNING"
    return "STABLE"

def main():
    parser = argparse.ArgumentParser(description="Clinivora Sepsis Diagnosis Tool")
    
    # Vitals
    parser.add_argument("--hr", type=float, help="Heart Rate (bpm)")
    parser.add_argument("--sbp", type=float, help="Systolic BP (mmHg)")
    parser.add_argument("--map", type=float, help="Mean Arterial Pressure (mmHg)")
    parser.add_argument("--o2", type=float, help="O2 Saturation (%)")
    parser.add_argument("--temp", type=float, help="Temperature (C)")
    parser.add_argument("--resp", type=float, help="Respiration Rate (bpm)")
    
    # Labs / Context
    parser.add_argument("--lactate", type=float, help="Lactate (mmol/L)")
    parser.add_argument("--wbc", type=float, help="White Blood Cell Count (k/uL)")
    parser.add_argument("--age", type=float, default=60.0, help="Age (years)")
    parser.add_argument("--gender", type=int, default=1, help="Gender (1=M, 0=F)")
    
    args = parser.parse_args()
    
    # Build Data Dictionary
    data = {}
    if args.hr: data['HR'] = args.hr
    if args.sbp: data['SBP'] = args.sbp
    if args.map: data['MAP'] = args.map
    if args.o2: data['O2Sat'] = args.o2
    if args.temp: data['Temp'] = args.temp
    if args.resp: data['Resp'] = args.resp
    if args.lactate: data['Lactate'] = args.lactate
    if args.wbc: data['WBC'] = args.wbc
    data['Age'] = args.age
    
    # Load Model
    model_path = os.path.join(os.path.dirname(__file__), 'sepsis_xgboost.pkl')
    try:
        predictor = SepsisPredictor(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Predict
    print("\n--- Clinivora Diagnostics ---")
    print(f"Input Vitals: {data}")
    
    raw_prob = predictor.predict(data)
    print(f"AI Raw Probability: {raw_prob:.3f}")
    
    final_prob, status, reason = apply_clinical_rules(raw_prob, data)
    risk = get_risk_label(final_prob)
    
    print("-" * 30)
    print(f"FINAL RISK: {risk}")
    print(f"Probability: {final_prob:.1%}")
    print(f"Status:     {status}")
    print(f"Reason:     {reason}")
    print("-" * 30)
    
    if risk == "CRITICAL":
        print("ACTION: IMMEDIATE ICU CONSULT + LACTATE TEST")
    elif risk == "WARNING":
        print("ACTION: INCREASE MONITORING FREQUENCY")
    else:
        print("ACTION: CONTINUE ROUTINE CARE")

if __name__ == "__main__":
    main()
