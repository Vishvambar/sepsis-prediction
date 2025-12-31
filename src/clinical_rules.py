
def apply_clinical_rules(prob, features):
    """
    Applies deterministic medical rules to override AI probability.
    
    Args:
        prob (float): The raw probability from the XGBoost model.
        features (dict): The dictionary of patient vitals/labs.
        
    Returns:
        tuple: (modified_prob, status, reason)
    """
    final_prob = prob
    reason = "Model Prediction"
    status = "AI_DERIVED"

    # RULE 1: Critical Lactate (Septic Shock Indicator)
    # Rationale: Lactate > 4.0 mmol/L is independent predictor of mortality
    lactate = features.get('Lactate')
    if lactate is not None and lactate >= 4.0:
        return 0.95, "OVERRIDE", "Critical Lactate (>= 4.0)"

    # RULE 2: Severe Bradycardia (Agonal State)
    # Rationale: HR < 40 is often pre-terminal, but AI mistakes it for 'athletic'
    hr = features.get('HR')
    if hr is not None and hr < 40:
        return 0.90, "OVERRIDE", "Severe Bradycardia (HR < 40)"
        
    # RULE 3: Severe Hypoxia (Safety Net for Respiratory Failure)
    o2 = features.get('O2Sat')
    if o2 is not None and o2 < 85:
         # Only override if the model missed it (prob < 0.7)
         if prob < 0.7:
            return 0.85, "OVERRIDE", "Severe Hypoxia (SpO2 < 85%)"

    # RULE 4: Hypotensive Shock (Safety Net)
    sbp = features.get('SBP')
    if sbp is not None and sbp < 90:
        # Override if model is asleep (prob < 0.22)
        if prob < 0.22:
            return 0.80, "OVERRIDE", "Severe Hypotension (SBP < 90)"

    return final_prob, status, reason
