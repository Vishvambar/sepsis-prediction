import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import roc_auc_score, average_precision_score, confusion_matrix, classification_report
import joblib
import os
import matplotlib.pyplot as plt
from data_loader import DataLoader

class SepsisModel:
    def __init__(self):
        self.model = None

    def train(self, X_train, y_train, X_val, y_val):
        print("Initializing XGBoost Classifier...")
        # Calculate scale_pos_weight
        ratio = float(np.sum(y_train == 0)) / np.sum(y_train == 1)
        print(f"Class Imbalance Ratio (Neg/Pos): {ratio:.2f}")

        self.model = xgb.XGBClassifier(
            objective='binary:logistic',
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            scale_pos_weight=ratio, # Handle imbalance,
            early_stopping_rounds=10,
            use_label_encoder=False,
            eval_metric='auc',
            random_state=42
        )

        print("Training model...")
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_train, y_train), (X_val, y_val)],
            verbose=True
        )
        print("Training complete.")

    def evaluate(self, X_test, y_test):
        print("\nEvaluating on Test Set...")
        y_probs = self.model.predict_proba(X_test)[:, 1]
        y_preds = self.model.predict(X_test)

        auc = roc_auc_score(y_test, y_probs)
        auprc = average_precision_score(y_test, y_probs)
        
        print(f"Test AUC-ROC: {auc:.4f}")
        print(f"Test AUPRC:   {auprc:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_preds))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_preds))

        # Identify Top Features
        importances = self.model.feature_importances_
        feature_names = X_test.columns
        feature_imp = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
        feature_imp = feature_imp.sort_values('Importance', ascending=False).head(10)
        print("\nTop 10 Features:")
        print(feature_imp)
        
        return auc, auprc

    def save_model(self, path='sepsis_xgboost.pkl'):
        print(f"Saving model to {path}...")
        joblib.dump(self.model, path)

if __name__ == "__main__":
    # Load and Preprocess
    loader = DataLoader(r'c:\Users\Admin\Desktop\mimic-iv-clinical-database-demo-2.2\Dataset.csv')
    loader.load_data()
    loader.preprocess()
    X_train, y_train, X_val, y_val, X_test, y_test = loader.split_data()

    # Train and Evaluate
    trainer = SepsisModel()
    trainer.train(X_train, y_train, X_val, y_val)
    trainer.evaluate(X_test, y_test)
    trainer.save_model(r'c:\Users\Admin\Desktop\mimic-iv-clinical-database-demo-2.2\src\sepsis_xgboost.model')
