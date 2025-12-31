
import pandas as pd
import numpy as np
import json
import os
import sys

# Ensure src is in path
sys.path.append(os.path.dirname(__file__))

from inference import SepsisPredictor
from clinical_rules import apply_clinical_rules

# --- CONFIGURATION ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'sepsis_xgboost.pkl')

def get_risk_label(prob):
    # CALIBRATED THRESHOLDS
    if prob >= 0.22: return "CRITICAL"
    if prob >= 0.08: return "WARNING"
    return "STABLE"

# --- SCENARIO DEFINITIONS ---
scenarios = [
    # --- GROUP A: STABLE BASLINE (Testing Specificity) ---
    # Goal: Ensure model output stays < 0.08
    {"id": 1, "desc": "Healthy Athlete", "history": [], 
     "data": {"HR": 50, "SBP": 110, "MAP": 80, "O2Sat": 99, "Temp": 36.5, "Resp": 14, "Age": 25, "Gender": 1}},

    {"id": 2, "desc": "Standard Admit", "history": [], 
     "data": {"HR": 70, "SBP": 120, "MAP": 90, "O2Sat": 98, "Temp": 37.0, "Resp": 16, "Age": 50, "Gender": 0}},

    {"id": 3, "desc": "Anxiety (High HR Only)", "history": [], 
     "data": {"HR": 105, "SBP": 130, "MAP": 95, "O2Sat": 99, "Temp": 37.0, "Resp": 18, "Age": 40}},

    {"id": 4, "desc": "Mild Fever (Flu)", "history": [], 
     "data": {"HR": 85, "SBP": 115, "MAP": 85, "O2Sat": 97, "Temp": 38.8, "Resp": 18, "Age": 35}},

    {"id": 5, "desc": "Post-Op Recovery", "history": [], 
     "data": {"HR": 80, "SBP": 105, "MAP": 75, "O2Sat": 96, "Temp": 36.8, "Resp": 16, "Age": 60}},


    # --- GROUP B: SILENT KILLERS (Testing AI Sensitivity) ---
    # Goal: Ensure model output is 0.08 - 0.22 (Warning) or > 0.22 (Critical)
    
    # 6. Compensated Sepsis: BP is normal, but HR is high and Fever is present.
    {"id": 6, "desc": "Compensated Sepsis", "history": [], 
     "data": {"HR": 115, "SBP": 115, "MAP": 85, "O2Sat": 94, "Temp": 38.9, "Resp": 24, "Age": 55}},

    # 7. Cold Sepsis: Elderly patient, no fever (hypothermic), confusing the layman but not the AI.
    {"id": 7, "desc": "Cold Sepsis (Elderly)", "history": [], 
     "data": {"HR": 95, "SBP": 100, "MAP": 70, "O2Sat": 92, "Temp": 35.5, "Resp": 22, "Age": 85}},

    # 8. Respiratory Sepsis: Pneumonia signs (Low O2, High Resp Rate).
    {"id": 8, "desc": "Respiratory Origin", "history": [], 
     "data": {"HR": 108, "SBP": 110, "MAP": 80, "O2Sat": 89, "Temp": 38.2, "Resp": 30, "Age": 65}},

    # 9. The Crash: Significant hypotension (Low BP) starting to show.
    {"id": 9, "desc": "Pre-Shock Crash", "history": [], 
     "data": {"HR": 120, "SBP": 88, "MAP": 62, "O2Sat": 93, "Temp": 39.0, "Resp": 26, "Age": 50}},

    # 10. Neutropenic Fever: Low WBC (immune failure) + Fever.
    {"id": 10, "desc": "Immunocompromised", "history": [], 
     "data": {"HR": 110, "SBP": 105, "MAP": 75, "O2Sat": 95, "Temp": 39.0, "WBC": 1.5, "Resp": 20}},


    # --- GROUP C: CLINICAL SAFETY RULES (Testing Overrides) ---
    # Goal: These MUST trigger CRITICAL via rules (Lactate, HR, O2)

    # 11. Hidden Killer: Vitals look okay, but Lactate is 4.5 (Cellular Death).
    {"id": 11, "desc": "High Lactate Hidden", "history": [], 
     "data": {"HR": 90, "SBP": 110, "MAP": 80, "O2Sat": 96, "Temp": 37.5, "Resp": 20, "Lactate": 4.5}},

    # 12. Septic Shock: Classic presentation (Low BP + High HR + Fever).
    {"id": 12, "desc": "Septic Shock", "history": [], 
     "data": {"HR": 135, "SBP": 75, "MAP": 55, "O2Sat": 90, "Temp": 39.5, "Resp": 32, "Lactate": 3.0}},

    # 13. Agonal State: Dying patient. HR < 40. AI might think "Athlete" without the rule.
    {"id": 13, "desc": "Agonal (Bradycardia)", "history": [], 
     "data": {"HR": 35, "SBP": 60, "MAP": 40, "O2Sat": 80, "Temp": 34.0, "Resp": 8}},

    # 14. Severe Hypoxia: O2 Saturation failing despite normal BP.
    {"id": 14, "desc": "Hypoxic Crisis", "history": [], 
     "data": {"HR": 115, "SBP": 120, "MAP": 85, "O2Sat": 82, "Temp": 37.5, "Resp": 35}},

    # 15. Multi-Organ Failure: Kidneys failing (Creatinine) + Liver (Bilirubin implied) + Shock.
    {"id": 15, "desc": "Multi-Organ Failure", "history": [], 
     "data": {"HR": 125, "SBP": 80, "MAP": 60, "O2Sat": 88, "Temp": 38.0, "Creatinine": 3.5, "Resp": 28}},


    # --- GROUP D: EDGE CASES (Testing Robustness) ---
    # Goal: Ensure code doesn't crash and gives reasonable estimates

    # 16. Missing Labs: Common scenario. Only vitals provided.
    {"id": 16, "desc": "Missing Labs", "history": [], 
     "data": {"HR": 110, "SBP": 100, "MAP": 70, "O2Sat": 94, "Temp": 38.0, "Resp": 22}},

    # 17. Extreme Age: 95yo patient (High baseline risk).
    {"id": 17, "desc": "Extreme Age (95)", "history": [], 
     "data": {"HR": 90, "SBP": 115, "MAP": 80, "O2Sat": 93, "Temp": 36.5, "Resp": 20, "Age": 95}},

    # 18. Young Adult: 19yo patient (Resilient).
    {"id": 18, "desc": "Young Adult (19)", "history": [], 
     "data": {"HR": 90, "SBP": 115, "MAP": 80, "O2Sat": 98, "Temp": 38.5, "Resp": 18, "Age": 19}},

    # 19. Data Typos: Strange but valid numbers (e.g. very low Temp).
    {"id": 19, "desc": "Data Entry Noise", "history": [], 
     "data": {"HR": 101, "SBP": 101, "MAP": 71, "O2Sat": 96, "Temp": 36.1, "Resp": 19}},

    # 20. Mixed Signals: Hypertension (High BP) + Hypoxia. Confusing picture.
    {"id": 20, "desc": "Mixed Signals", "history": [], 
     "data": {"HR": 100, "SBP": 170, "MAP": 110, "O2Sat": 88, "Temp": 37.5, "Resp": 24}}
]

def run_tests():
    print(f"Loading Model from {MODEL_PATH}...")
    try:
        predictor = SepsisPredictor(MODEL_PATH)
    except Exception as e:
        print(f"ERROR: Could not load model. {e}")
        return

    results = []
    print(f"\n{'ID':<4} | {'Scenario':<25} | {'Model Prob':<10} | {'Final Prob':<10} | {'Status':<10} | {'Reason'}")
    print("-" * 120)

    for case in scenarios:
        try:
            # 1. AI Prediction
            raw_prob = predictor.predict(case['data'], history=case.get('history', []))
            
            # 2. Apply Clinical Rules (Hybrid Intelligence)
            final_prob, status, reason = apply_clinical_rules(raw_prob, case['data'])
            
            risk_label = get_risk_label(final_prob)
            
            # Console Output
            desc = case['desc'][:25]
            row_fmt = f"{case['id']:<4} | {desc:<25} | {raw_prob:.3f}      | {final_prob:.3f}      | {status:<10} | {reason}"
            print(row_fmt)
            
            results.append(f"| {case['id']} | {case['desc']} | {raw_prob:.3f} | {final_prob:.3f} | **{risk_label}** | {status} | {reason} |")
            
        except Exception as e:
            print(f"{case['id']:<4} | {case['desc']:<25} | ERROR: {e}")

    # Generate Report
    with open("scenario_results_comprehensive.md", "w", encoding='utf-8') as f:
        f.write("# Clinivora Comprehensive Test Report\n\n")
        f.write("| ID | Scenario | AI Prob | Final Prob | Risk | Source | Reason |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        f.write("\n".join(results))
    
    print("\n[SUCCESS] Comprehensive Test Complete. Report saved to 'scenario_results_comprehensive.md'")

if __name__ == "__main__":
    run_tests()
