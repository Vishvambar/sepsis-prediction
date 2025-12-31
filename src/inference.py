import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
import json
import os

class SepsisPredictor:
    def __init__(self, model_path):
        # Load Model
        print(f"Loading model from: {model_path}")
        try:
            self.model = joblib.load(model_path)
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

        # Robust Feature Loading
        # Try appending .features to the exact path provided
        feature_path = model_path + ".features"
        
        try:
            self.feature_names = joblib.load(feature_path)
            print(f"[SUCCESS] Features loaded from: {feature_path}")
            print(f"   (Expecting {len(self.feature_names)} features)")
        except FileNotFoundError:
            print(f"[CRITICAL ERROR] Could not find {feature_path}")
            print("   The model needs this file to map 'Age' and 'HR' correctly.")
            self.feature_names = []
        except Exception as e:
            print(f"Warning: Could not load feature names: {e}") 
            self.feature_names = [] 

        # Validate against Booster
        try:
             booster = self.model.get_booster()
             booster_feats = booster.feature_names
             if booster_feats:
                 print(f"DEBUG: Booster expects {len(booster_feats)} features")
                 # If file loaded 60 but booster needs valid subset, prefer booster?
                 if self.feature_names and self.feature_names != booster_feats:
                     print(f"DEBUG: MISMATCH! File has {len(self.feature_names)}, Booster has {len(booster_feats)}")
                     print(f"DEBUG: Booster Features: {booster_feats[:5]}...")
                     # FORCE USE BOOSTER FEATURES
                     self.feature_names = booster_feats
                     print("DEBUG: Overwrote feature_names with booster source of truth.")
        except Exception as e:
             print(f"DEBUG: Could not validate booster features: {e}") 

    def predict(self, current_data, history=None, baseline=None):
        """
        current_data: dict of current vitals/labs
        history: list of dicts (past hours) - optional
        baseline: dict of admission vitals - optional
        """
        
        # 1. cold Start Logic
        # If no history, we cannot calculate Lag1 or Rolling.
        # Assumption: Lag1 = Current (Delta=0), Rolling = Current (Stable)
        
        features = current_data.copy()
        
        # Vitals to engineer
        vitals = ['HR', 'MAP', 'SBP', 'O2Sat', 'Temp', 'Resp'] # Must match training list
        
        for v in vitals:
            val = features.get(v, np.nan) # Current value
            
            # Lag 1
            if history and len(history) > 0:
                lag1 = history[-1].get(v, val) # Last hour
            else:
                lag1 = val # Assumption: Stable
            
            features[f'{v}_Lag1'] = lag1
            
            # Delta
            features[f'{v}_Delta'] = val - lag1
            
            # Rolling (Approximation for MVP: Average of History + Current)
            if history:
                hist_vals = [h.get(v, val) for h in history[-5:]] # Last 5 + current = 6
                hist_vals.append(val)
                roll_mean = np.mean(hist_vals)
            else:
                roll_mean = val # Assumption: Stable
                
            features[f'{v}_RollMean6h'] = roll_mean

        # Convert to DataFrame
        df = pd.DataFrame([features])
        
        # FIX: The model was trained on ALL columns (Laboratories, Demographics, etc.)
        # We must provide all columns. For missing Labs/Demographics, we pass NaN 
        # (XGBoost handles missing values automatically).
        
        try:
            # 1. Determine Model's Expected Columns
            expected_features = self.feature_names
            if expected_features is None:
                booster = self.model.get_booster()
                expected_features = booster.feature_names
            
            # 2. [NEW] SMART MAPPING (Case-Insensitive Logic)
            # Create a dictionary mapping { 'age': 'Age', 'hr': 'HR', ... } based on MODEL's needs
            if expected_features:
                model_cols_map = {c.strip().lower(): c for c in expected_features}
            else:
                model_cols_map = {}
            
            # Create a new standardized dictionary for the dataframe
            mapped_data = {}
            
            # Loop through your INPUT data and map it to the MODEL's column names
            # (We look at the 'features' dict we built earlier with Lags/Deltas)
            for input_col, val in features.items():
                norm_input = input_col.strip().lower()
                if norm_input in model_cols_map:
                    target_col = model_cols_map[norm_input]
                    mapped_data[target_col] = val
            
            # 3. Create DataFrame from the MAPPED data
            # If mapping found nothing (empty map or no match), fallback to using features directly? 
            # The logic implies we only trust mapped cols. If mapped_data is empty, use features to be safe?
            # User instructions say "Create DataFrame from the MAPPED data". 
            # If we strictly follow, any unmapped col is dropped. This is safer for reindex.
            if not mapped_data and features:
                 # Fallback: if no features were mapped (maybe model_cols_map is empty?), use raw
                 if not model_cols_map:
                     df = pd.DataFrame([features])
                 else:
                     df = pd.DataFrame([mapped_data])
            else:
                df = pd.DataFrame([mapped_data])

            # 4. Apply Defaults (Only if missing from mapped data)
            defaults = {
                'Age': 60.0, 'Gender': 1, 'ICULOS': 24.0, 
                'Hour': 12.0, 'HospAdmTime': -24.0
            }
            # We must map defaults to the model's casing too
            for def_col, def_val in defaults.items():
                norm_def = def_col.strip().lower()
                if norm_def in model_cols_map:
                    target_col = model_cols_map[norm_def]
                    if target_col not in df.columns:
                        df[target_col] = def_val

            # 5. Reindex (Now safe because names match)
            if expected_features:
                # Debug print removed to reduce noise, or keep if useful? Keeping clean per request
                # print(f"DEBUG: Reindexing df to {len(expected_features)} columns")
                df = df.reindex(columns=expected_features, fill_value=np.nan)
            
            # 6. Type Conversion & Prediction
            df = df.apply(pd.to_numeric, errors='coerce')
            prob = self.model.predict_proba(df)[:, 1][0]
            
            return float(prob)

        except Exception as e:
            print(f"Prediction error: {e}")
            return 0.0

if __name__ == "__main__":
    # Test Cold Start
    # Use relative path assuming we run from project root or src
    path = os.path.join(os.path.dirname(__file__), 'sepsis_xgboost.pkl')
    pred = SepsisPredictor(path)
    current = {'HR': 100, 'MAP': 65, 'SBP': 90, 'O2Sat': 92, 'Temp': 38.5, 'Resp': 22}
    print(f"Prediction (Cold Start): {pred.predict(current)}")
