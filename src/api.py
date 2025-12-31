
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import os
import sys

# Add src to path if needed (though typically this runs from root)
sys.path.append(os.path.dirname(__file__))

from inference import SepsisPredictor
from clinical_rules import apply_clinical_rules

app = FastAPI(title="Clinivora Sepsis API", version="1.0")

# Initialize Predictor
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'sepsis_xgboost.pkl')
try:
    predictor = SepsisPredictor(MODEL_PATH)
except Exception as e:
    print(f"CRITICAL ERROR: Failed to load model: {e}")
    predictor = None

class VitalsInput(BaseModel):
    HR: Optional[float] = None
    SBP: Optional[float] = None
    MAP: Optional[float] = None
    O2Sat: Optional[float] = None
    Temp: Optional[float] = None
    Resp: Optional[float] = None
    Lactate: Optional[float] = None
    WBC: Optional[float] = None
    GCS: Optional[float] = None
    Age: Optional[float] = None
    ICULOS: Optional[float] = None
    # Flexible dict to catch any other optional features
    class Config:
        extra = "allow"

@app.get("/")
def health_check():
    return {"status": "online", "model_loaded": predictor is not None}

@app.post("/predict")
def predict_sepsis(data: VitalsInput):
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # Filter out None values so they don't overwrite actual data in Smart Mapping
    current_data = {k: v for k, v in data.dict().items() if v is not None}
    print(f"DEBUG: API received payload: {current_data}")
    
    # 1. Run Inference
    # Note: connect history/baseline if API evolves, for now stateless
    raw_prob = predictor.predict(current_data)
    
    # 2. Apply Clinical Rules (Hybrid Layer)
    final_prob, status_source, rule_reason = apply_clinical_rules(raw_prob, current_data)
    
    # 3. Calibrate Risk Levels (The "Whisper" Fix)
    if final_prob >= 0.22:
        risk_label = "CRITICAL"
        action = "Immediate ICU Consult + Lactate Test"
    elif final_prob >= 0.08:
        risk_label = "WARNING"
        action = "Increase Monitoring Frequency"
    else:
        risk_label = "STABLE"
        action = "Continue Routine Care"

    # Formatting for UI
    return {
        "diagnosis": risk_label,
        "risk_score": f"{final_prob * 100:.1f}%",
        "raw_probability": final_prob,
        "action": action,
        "alert": rule_reason if status_source == "OVERRIDE" else None,
        "source": status_source
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
