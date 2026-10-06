#!/usr/bin/env python3
"""
Train initial lightweight baseline models:
- Logistic Regression
- Decision Tree

Requires outputs/train.csv and outputs/validation.csv
created by preprocess_data.py.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.tree import DecisionTreeClassifier

NON_FEATURE_COLUMNS = {"url", "label"}


def split_xy(df: pd.DataFrame):
    feature_cols = [c for c in df.columns if c not in NON_FEATURE_COLUMNS]
    X = df[feature_cols]
    y = df["label"]
    return X, y, feature_cols


def evaluate(model, X, y):
    start = time.perf_counter()
    preds = model.predict(X)
    elapsed = time.perf_counter() - start

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X)[:, 1]
        roc_auc = roc_auc_score(y, probs)
    else:
        roc_auc = None

    return {
        "accuracy": accuracy_score(y, preds),
        "precision": precision_score(y, preds, zero_division=0),
        "recall": recall_score(y, preds, zero_division=0),
        "f1": f1_score(y, preds, zero_division=0),
        "roc_auc": roc_auc,
        "inference_seconds_total": elapsed,
        "inference_seconds_per_url": elapsed / max(len(X), 1),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", default="outputs/train.csv")
    parser.add_argument("--validation", default="outputs/validation.csv")
    parser.add_argument("--model-dir", default="models")
    parser.add_argument("--results-dir", default="outputs")
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    train_df = pd.read_csv(args.train)
    val_df = pd.read_csv(args.validation)

    X_train, y_train, feature_cols = split_xy(train_df)
    X_val = val_df[feature_cols]
    y_val = val_df["label"]

    models = {
        "logistic_regression": LogisticRegression(
            max_iter=1000,
            random_state=args.random_state
        ),
        "decision_tree": DecisionTreeClassifier(
            random_state=args.random_state,
            max_depth=12
        ),
    }

    model_dir = Path(args.model_dir)
    results_dir = Path(args.results_dir)
    model_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    results = {}

    for name, model in models.items():
        model.fit(X_train, y_train)

        model_path = model_dir / f"{name}.joblib"
        joblib.dump(model, model_path)

        metrics = evaluate(model, X_val, y_val)
        metrics["model_size_bytes"] = model_path.stat().st_size
        results[name] = metrics

        print(f"\n{name}")
        for key, value in metrics.items():
            print(f"  {key}: {value}")

    with open(results_dir / "validation_metrics.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nSaved models and validation metrics.")


if __name__ == "__main__":
    main()
