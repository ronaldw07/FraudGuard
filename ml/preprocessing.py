# Author: Ronald Wen
# preprocessing.py - Data loading, scaling, and oversampling for fraud detection

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import joblib

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'creditcard.csv')
SCALER_PATH = os.path.join(os.path.dirname(__file__), '..', 'backend', 'model', 'scaler.pkl')


def load_and_preprocess():
    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=['Class'])
    y = df['Class']

    # Scale Time and Amount (V1-V28 are already PCA-transformed)
    scaler = StandardScaler()
    X[['Time', 'Amount']] = scaler.fit_transform(X[['Time', 'Amount']])

    # Stratified 80/20 split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training set size: {len(X_train)}, Test set size: {len(X_test)}")
    print(f"Fraud cases in training set before SMOTE: {y_train.sum()}")

    # Apply SMOTE only on training data
    # sampling_strategy=0.1 caps fraud at 10% of majority class (~22k rows) instead of full balance (~450k rows)
    smote = SMOTE(random_state=42, sampling_strategy=0.1)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

    print(f"Training set size after SMOTE: {len(X_train_resampled)}")
    print(f"Fraud cases after SMOTE: {y_train_resampled.sum()}")

    # Save scaler
    os.makedirs(os.path.dirname(SCALER_PATH), exist_ok=True)
    joblib.dump(scaler, SCALER_PATH)
    print(f"Scaler saved to {SCALER_PATH}")

    return X_train_resampled, X_test, y_train_resampled, y_test, scaler


if __name__ == '__main__':
    load_and_preprocess()
