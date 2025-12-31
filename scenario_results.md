# Sepsis Model Scenario Test Report
Date: 2025-12-25 18:03:17.596783

| ID | Scenario | Expected | Prob | Risk Level | Result |
|----|----------|----------|------|------------|--------|
| 01 | The Athlete | STABLE | 0.0384 | **STABLE** | ✅ |
| 02 | The Standard Admit | STABLE | 0.0542 | **WARNING** | ⚠️ |
| 03 | Anxiety/Stress | STABLE/WATCH | 0.1224 | **WARNING** | ⚠️ |
| 04 | Mild Fever | STABLE/WATCH | 0.1469 | **WARNING** | ⚠️ |
| 05 | Post-Op Recovery | STABLE | 0.0701 | **WARNING** | ⚠️ |
| 06 | Compensated Sepsis | WARNING / HIGH | 0.1268 | **WARNING** | ✅ |
| 07 | Cold Sepsis | HIGH RISK | 0.2590 | **CRITICAL** | ⚠️ |
| 08 | Respiratory Origin | HIGH RISK | 0.1988 | **CRITICAL** | ⚠️ |
| 09 | The Crash Phase | CRITICAL | 0.2841 | **CRITICAL** | ✅ |
| 10 | High Lactate | CRITICAL | 0.0375 | **STABLE** | ⚠️ |
| 11 | Septic Shock | CRITICAL | 0.2375 | **CRITICAL** | ✅ |
| 12 | Multi-Organ Failure | CRITICAL | 0.4718 | **CRITICAL** | ✅ |
| 13 | Systemic Infection | HIGH / CRITICAL | 0.2241 | **CRITICAL** | ✅ |
| 14 | Hypoxic Crisis | CRITICAL | 0.2618 | **CRITICAL** | ✅ |
| 15 | Agonal State | CRITICAL | 0.0157 | **STABLE** | ⚠️ |
| 16 | Missing Labs | Valid Prediction | 0.1330 | **WARNING** | ✅ |
| 17 | Extreme Age | Higher Risk Baseline | 0.3551 | **CRITICAL** | ✅ |
| 18 | Young Adult | Lower Risk Baseline | 0.0426 | **STABLE** | ✅ |
| 19 | Data Entry Typos | Valid Prediction | 0.0621 | **WARNING** | ✅ |
| 20 | Mixed Signals | WARNING | 0.1455 | **WARNING** | ✅ |