#!/usr/bin/env python3
"""
Evaluate saved Logistic Regression and Decision Tree models
on the held-out test set using one common evaluation process.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)

NON_FEATURE_COLUMNS = {"url", "label"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", default="outputs/test.csv")
    parser.add_argument("--model-dir", default="models")
    parser.add_argument("--output", default="outputs/test_metrics.json")
    args = parser.parse_args()

    test_df = pd.read_csv(args.test)
    feature_cols = [c for c in test_df.columns if c not in NON_FEATURE_COLUMNS]
    X_test = test_df[feature_cols]
    y_test = test_df["label"]

    model_paths = {
        "logistic_regression": Path(args.model_dir) / "logistic_regression.joblib",
        "decision_tree": Path(args.model_dir) / "decision_tree.joblib",
    }

    results = {}

    for name, path in model_paths.items():
        model = joblib.load(path)

        start = time.perf_counter()
        preds = model.predict(X_test)
        elapsed = time.perf_counter() - start

        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X_test)[:, 1]
            roc_auc = roc_auc_score(y_test, probs)
        else:
            roc_auc = None

        results[name] = {
            "accuracy": accuracy_score(y_test, preds),
            "precision": precision_score(y_test, preds, zero_division=0),
            "recall": recall_score(y_test, preds, zero_division=0),
            "f1": f1_score(y_test, preds, zero_division=0),
            "roc_auc": roc_auc,
            "confusion_matrix": confusion_matrix(y_test, preds).tolist(),
            "inference_seconds_total": elapsed,
            "inference_seconds_per_url": elapsed / max(len(X_test), 1),
            "model_size_bytes": path.stat().st_size,
        }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
