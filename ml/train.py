# Author: Ronald Wen
# train.py - XGBoost model training with hyperparameter tuning and MLflow logging

import os
import joblib
import mlflow
import mlflow.xgboost
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from sklearn.metrics import roc_auc_score, f1_score

from preprocessing import load_and_preprocess

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'backend', 'model', 'model.pkl')

PARAM_DIST = {
    'max_depth': [3, 4, 5, 6, 7, 8],
    'learning_rate': [0.01, 0.05, 0.1, 0.2, 0.3],
    'n_estimators': [100, 200, 300, 500],
    'subsample': [0.6, 0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.6, 0.7, 0.8, 0.9, 1.0],
}


def train():
    X_train, X_test, y_train, y_test, _ = load_and_preprocess()

    mlflow.set_experiment("fraudguard-xgboost")

    with mlflow.start_run(run_name="randomized_search"):
        base_model = XGBClassifier(
            use_label_encoder=False,
            eval_metric='logloss',
            random_state=42,
            n_jobs=2,          # limit to 2 cores to avoid memory/CPU spike
            tree_method='hist', # faster, lower memory than exact
        )

        cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)  # 3-fold instead of 5

        search = RandomizedSearchCV(
            estimator=base_model,
            param_distributions=PARAM_DIST,
            n_iter=5,          # 5 iterations instead of 20
            scoring='roc_auc',
            cv=cv,
            verbose=2,
            random_state=42,
            n_jobs=1,          # run CV jobs sequentially
        )

        print("Starting hyperparameter search...")
        search.fit(X_train, y_train)

        best_model = search.best_estimator_
        best_params = search.best_params_

        print(f"Best params: {best_params}")

        y_pred_proba = best_model.predict_proba(X_test)[:, 1]
        y_pred = best_model.predict(X_test)

        auc = roc_auc_score(y_test, y_pred_proba)
        f1 = f1_score(y_test, y_pred)

        print(f"AUC-ROC: {auc:.4f}")
        print(f"F1 Score: {f1:.4f}")

        mlflow.log_params(best_params)
        mlflow.log_metric("auc_roc", auc)
        mlflow.log_metric("f1_score", f1)
        mlflow.xgboost.log_model(best_model, "model")

        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(best_model, MODEL_PATH)
        print(f"Model saved to {MODEL_PATH}")

    return best_model, X_test, y_test


if __name__ == '__main__':
    train()
