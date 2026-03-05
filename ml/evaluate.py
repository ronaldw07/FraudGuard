# Author: Ronald Wen
# evaluate.py - Model evaluation, threshold optimization, and metric reporting

import os
import json
import joblib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import (
    roc_auc_score, f1_score, precision_score, recall_score,
    average_precision_score, precision_recall_curve,
)

from preprocessing import load_and_preprocess

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'backend', 'model', 'model.pkl')
THRESHOLD_PATH = os.path.join(os.path.dirname(__file__), '..', 'backend', 'model', 'threshold.json')
PR_CURVE_PATH = os.path.join(os.path.dirname(__file__), 'outputs', 'pr_curve.png')


def evaluate():
    _, X_test, _, y_test, _ = load_and_preprocess()

    model = joblib.load(MODEL_PATH)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    auc = roc_auc_score(y_test, y_pred_proba)
    avg_precision = average_precision_score(y_test, y_pred_proba)

    print(f"AUC-ROC: {auc:.4f}")
    print(f"Average Precision: {avg_precision:.4f}")

    # Sweep thresholds to find optimal F1
    thresholds = np.arange(0.1, 0.91, 0.05)
    best_f1 = 0.0
    best_threshold = 0.5

    print("\nThreshold sweep:")
    for t in thresholds:
        y_pred = (y_pred_proba >= t).astype(int)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        print(f"  threshold={t:.2f}  F1={f1:.4f}  Precision={prec:.4f}  Recall={rec:.4f}")
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = float(t)

    print(f"\nOptimal threshold: {best_threshold:.2f} (F1={best_f1:.4f})")

    # Save optimal threshold
    os.makedirs(os.path.dirname(THRESHOLD_PATH), exist_ok=True)
    with open(THRESHOLD_PATH, 'w') as f:
        json.dump({'threshold': best_threshold}, f)
    print(f"Threshold saved to {THRESHOLD_PATH}")

    # Plot precision-recall curve
    precision_vals, recall_vals, _ = precision_recall_curve(y_test, y_pred_proba)

    os.makedirs(os.path.dirname(PR_CURVE_PATH), exist_ok=True)
    plt.figure(figsize=(8, 6))
    plt.plot(recall_vals, precision_vals, color='steelblue', lw=2)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PR_CURVE_PATH, dpi=150)
    plt.close()
    print(f"Precision-recall curve saved to {PR_CURVE_PATH}")

    # Final metrics at optimal threshold
    y_pred_final = (y_pred_proba >= best_threshold).astype(int)
    print("\nFinal metrics at optimal threshold:")
    print(f"  F1:        {f1_score(y_test, y_pred_final):.4f}")
    print(f"  Precision: {precision_score(y_test, y_pred_final):.4f}")
    print(f"  Recall:    {recall_score(y_test, y_pred_final):.4f}")


if __name__ == '__main__':
    evaluate()
