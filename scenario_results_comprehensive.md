# Clinivora Comprehensive Test Report

| ID | Scenario | AI Prob | Final Prob | Risk | Source | Reason |
|---|---|---|---|---|---|---|
| 1 | Healthy Athlete | 0.011 | 0.011 | **STABLE** | AI_DERIVED | Model Prediction |
| 2 | Standard Admit | 0.003 | 0.003 | **STABLE** | AI_DERIVED | Model Prediction |
| 3 | Anxiety (High HR Only) | 0.002 | 0.002 | **STABLE** | AI_DERIVED | Model Prediction |
| 4 | Mild Fever (Flu) | 0.002 | 0.002 | **STABLE** | AI_DERIVED | Model Prediction |
| 5 | Post-Op Recovery | 0.008 | 0.008 | **STABLE** | AI_DERIVED | Model Prediction |
| 6 | Compensated Sepsis | 0.003 | 0.003 | **STABLE** | AI_DERIVED | Model Prediction |
| 7 | Cold Sepsis (Elderly) | 0.014 | 0.014 | **STABLE** | AI_DERIVED | Model Prediction |
| 8 | Respiratory Origin | 0.001 | 0.001 | **STABLE** | AI_DERIVED | Model Prediction |
| 9 | Pre-Shock Crash | 0.008 | 0.800 | **CRITICAL** | OVERRIDE | Severe Hypotension (SBP < 90) |
| 10 | Immunocompromised | 0.005 | 0.005 | **STABLE** | AI_DERIVED | Model Prediction |
| 11 | High Lactate Hidden | 0.003 | 0.950 | **CRITICAL** | OVERRIDE | Critical Lactate (>= 4.0) |
| 12 | Septic Shock | 0.004 | 0.800 | **CRITICAL** | OVERRIDE | Severe Hypotension (SBP < 90) |
| 13 | Agonal (Bradycardia) | 0.010 | 0.900 | **CRITICAL** | OVERRIDE | Severe Bradycardia (HR < 40) |
| 14 | Hypoxic Crisis | 0.002 | 0.850 | **CRITICAL** | OVERRIDE | Severe Hypoxia (SpO2 < 85%) |
| 15 | Multi-Organ Failure | 0.004 | 0.800 | **CRITICAL** | OVERRIDE | Severe Hypotension (SBP < 90) |
| 16 | Missing Labs | 0.003 | 0.003 | **STABLE** | AI_DERIVED | Model Prediction |
| 17 | Extreme Age (95) | 0.006 | 0.006 | **STABLE** | AI_DERIVED | Model Prediction |
| 18 | Young Adult (19) | 0.002 | 0.002 | **STABLE** | AI_DERIVED | Model Prediction |
| 19 | Data Entry Noise | 0.012 | 0.012 | **STABLE** | AI_DERIVED | Model Prediction |
| 20 | Mixed Signals | 0.003 | 0.003 | **STABLE** | AI_DERIVED | Model Prediction |