# Clinivora Hybrid Intelligence Report

| ID | Scenario | AI Prob | Final Prob | Risk | Source | Reason |
|---|---|---|---|---|---|---|
| 01 | The Athlete | 0.038 | 0.038 | **STABLE** | AI_DERIVED | Model Prediction |
| 02 | The Standard Admit | 0.054 | 0.054 | **STABLE** | AI_DERIVED | Model Prediction |
| 03 | Anxiety/Stress | 0.122 | 0.122 | **WARNING** | AI_DERIVED | Model Prediction |
| 04 | Mild Fever | 0.147 | 0.147 | **WARNING** | AI_DERIVED | Model Prediction |
| 05 | Post-Op Recovery | 0.070 | 0.070 | **STABLE** | AI_DERIVED | Model Prediction |
| 06 | Compensated Sepsis | 0.127 | 0.127 | **WARNING** | AI_DERIVED | Model Prediction |
| 07 | Cold Sepsis | 0.259 | 0.259 | **CRITICAL** | AI_DERIVED | Model Prediction |
| 08 | Respiratory Origin | 0.199 | 0.199 | **WARNING** | AI_DERIVED | Model Prediction |
| 09 | The Crash Phase | 0.284 | 0.284 | **CRITICAL** | AI_DERIVED | Model Prediction |
| 10 | High Lactate Hidden | 0.038 | 0.950 | **CRITICAL** | OVERRIDE | Critical Lactate (>= 4.0) |
| 11 | Septic Shock | 0.238 | 0.238 | **CRITICAL** | AI_DERIVED | Model Prediction |
| 12 | Multi-Organ Failure | 0.472 | 0.472 | **CRITICAL** | AI_DERIVED | Model Prediction |
| 13 | Systemic Infection | 0.224 | 0.224 | **CRITICAL** | AI_DERIVED | Model Prediction |
| 14 | Hypoxic Crisis | 0.262 | 0.850 | **CRITICAL** | OVERRIDE | Severe Hypoxia (SpO2 < 85%) |
| 15 | Agonal (Dying) | 0.016 | 0.900 | **CRITICAL** | OVERRIDE | Severe Bradycardia (HR < 40) |
| 16 | Missing Labs | 0.133 | 0.133 | **WARNING** | AI_DERIVED | Model Prediction |
| 17 | Extreme Age | 0.355 | 0.355 | **CRITICAL** | AI_DERIVED | Model Prediction |
| 18 | Young Adult | 0.043 | 0.043 | **STABLE** | AI_DERIVED | Model Prediction |
| 19 | Data Entry Typos | 0.062 | 0.062 | **STABLE** | AI_DERIVED | Model Prediction |
| 20 | Mixed Signals | 0.146 | 0.146 | **WARNING** | AI_DERIVED | Model Prediction |
| 21 | Normal Vitals + AMS | 0.076 | 0.076 | **STABLE** | AI_DERIVED | Model Prediction |
| 22 | Hypothermia Sepsis | 0.254 | 0.254 | **CRITICAL** | AI_DERIVED | Model Prediction |
| 23 | Compensated Shock | 0.206 | 0.206 | **WARNING** | AI_DERIVED | Model Prediction |
| 24 | Neutropenic Fever | 0.225 | 0.225 | **CRITICAL** | AI_DERIVED | Model Prediction |
| 25 | Severe Hypoxia | 0.157 | 0.850 | **CRITICAL** | OVERRIDE | Severe Hypoxia (SpO2 < 85%) |