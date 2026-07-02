# Author: Ronald Wen
# explainability.py - SHAP-based feature attribution for model predictions

import pandas as pd
import shap

_explainer = None
_explainer_model_id = None


def _get_explainer(model) -> shap.TreeExplainer:
    global _explainer, _explainer_model_id
    if _explainer is None or _explainer_model_id != id(model):
        _explainer = shap.TreeExplainer(model)
        _explainer_model_id = id(model)
    return _explainer


def get_shap_values(model, input_df: pd.DataFrame) -> dict:
    """
    Compute SHAP values for a single transaction input.

    Returns top 5 feature contributions as a dict with:
      - feature: feature name
      - shap_value: raw SHAP value (float)
      - direction: 'increases' or 'decreases' fraud risk
    """
    explainer = _get_explainer(model)

    shap_values = explainer.shap_values(input_df)

    # For binary classification, shap_values may be a list [class0, class1]
    if isinstance(shap_values, list):
        values = shap_values[1][0]
    else:
        values = shap_values[0]

    feature_names = input_df.columns.tolist()
    contributions = []
    for name, val in zip(feature_names, values):
        contributions.append({
            'feature': name,
            'shap_value': float(val),
            'direction': 'increases' if val > 0 else 'decreases',
        })

    # Sort by absolute SHAP value, return top 5
    contributions.sort(key=lambda x: abs(x['shap_value']), reverse=True)
    return {'top_features': contributions[:5]}
