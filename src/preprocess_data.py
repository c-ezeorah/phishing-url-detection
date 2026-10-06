#!/usr/bin/env python3
"""
Preprocess a labeled phishing-URL dataset.

What this script does:
- loads a CSV file
- keeps URL + label columns
- drops missing / blank rows
- removes duplicate URLs
- normalizes common label formats to 0/1
- extracts lightweight lexical URL features
- creates reproducible train/validation/test splits
- writes processed CSV files to outputs/

Example:
    python src/preprocess_data.py \
        --input data/urls.csv \
        --url-column url \
        --label-column label
"""

from __future__ import annotations

import argparse
import ipaddress
import re
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
from sklearn.model_selection import train_test_split

URL_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly",
    "buff.ly", "is.gd", "cutt.ly", "rb.gy", "rebrand.ly"
}


def normalize_url(url: str) -> str:
    url = str(url).strip()
    if not url:
        return ""
    if "://" not in url:
        url = "http://" + url
    return url


def contains_ip_address(host: str) -> int:
    if not host:
        return 0
    try:
        ipaddress.ip_address(host)
        return 1
    except ValueError:
        return 0


def count_special_characters(text: str) -> int:
    return sum(not ch.isalnum() for ch in text)


def extract_lexical_features(url: str) -> dict:
    raw = str(url).strip()
    normalized = normalize_url(raw)
    parsed = urlparse(normalized)
    host = (parsed.hostname or "").lower()

    return {
        "url_length": len(raw),
        "hostname_length": len(host),
        "num_dots": raw.count("."),
        "num_hyphens": raw.count("-"),
        "num_question_marks": raw.count("?"),
        "num_equal_signs": raw.count("="),
        "num_digits": sum(ch.isdigit() for ch in raw),
        "num_special_chars": count_special_characters(raw),
        "uses_https": int(raw.lower().startswith("https://")),
        "contains_ip_address": contains_ip_address(host),
        "uses_known_shortener": int(host in URL_SHORTENERS),
    }


def normalize_label(value):
    """
    Converts common benign/phishing label formats to:
      0 = legitimate / benign
      1 = phishing / malicious
    """
    if pd.isna(value):
        return None

    if isinstance(value, (int, float)):
        if value in (0, 1):
            return int(value)
        if value == -1:
            return 1

    text = str(value).strip().lower()

    benign = {"0", "benign", "legitimate", "safe", "good"}
    phishing = {"1", "-1", "phishing", "malicious", "bad", "unsafe"}

    if text in benign:
        return 0
    if text in phishing:
        return 1

    raise ValueError(f"Unrecognized label value: {value!r}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input CSV file")
    parser.add_argument("--url-column", default="url")
    parser.add_argument("--label-column", default="label")
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    input_path = Path(args.input)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    missing = [c for c in (args.url_column, args.label_column) if c not in df.columns]
    if missing:
        raise KeyError(
            f"Missing required columns: {missing}. "
            f"Available columns: {list(df.columns)}"
        )

    df = df[[args.url_column, args.label_column]].copy()
    df.columns = ["url", "label"]

    # Basic cleaning
    df = df.dropna(subset=["url", "label"])
    df["url"] = df["url"].astype(str).str.strip()
    df = df[df["url"] != ""]
    df = df.drop_duplicates(subset=["url"]).reset_index(drop=True)

    # Normalize labels
    df["label"] = df["label"].apply(normalize_label)
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)

    # Feature extraction
    feature_rows = [extract_lexical_features(url) for url in df["url"]]
    feature_df = pd.DataFrame(feature_rows)

    processed = pd.concat(
        [df[["url", "label"]].reset_index(drop=True), feature_df],
        axis=1
    )

    # Reproducible 70/15/15 split
    train_df, temp_df = train_test_split(
        processed,
        test_size=0.30,
        random_state=args.random_state,
        stratify=processed["label"],
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        random_state=args.random_state,
        stratify=temp_df["label"],
    )

    processed.to_csv(out_dir / "processed_features.csv", index=False)
    train_df.to_csv(out_dir / "train.csv", index=False)
    val_df.to_csv(out_dir / "validation.csv", index=False)
    test_df.to_csv(out_dir / "test.csv", index=False)

    print("Preprocessing complete.")
    print(f"Total usable rows: {len(processed)}")
    print(f"Train: {len(train_df)}")
    print(f"Validation: {len(val_df)}")
    print(f"Test: {len(test_df)}")
    print("\nClass distribution:")
    print(processed["label"].value_counts(normalize=True).sort_index())


if __name__ == "__main__":
    main()
