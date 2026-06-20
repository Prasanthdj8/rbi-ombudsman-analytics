"""
classify_complaints.py

Text classifier that tags complaint-style text into RBI's published Ombudsman
complaint categories (Loans and Advances, Credit Cards, ATM/Debit Cards,
Mobile/Electronic Banking, Deposit Accounts, Pension Related).

Trained on synthetic_complaints.csv (see generate_synthetic_complaints.py and
README.md for full disclosure on data provenance).

Pipeline: TF-IDF vectorization -> Linear SVM, with a held-out test split and
a classification report. This mirrors the kind of lightweight, explainable
classification pipeline appropriate for an internal MIS / dashboard tool,
where interpretability and speed matter more than marginal accuracy gains
from a larger model.

Usage:
    python classify_complaints.py
"""

import csv
import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
import joblib


def load_data(path: str):
    texts, labels = [], []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts.append(row["text"])
            labels.append(row["category"])
    return texts, labels


def build_pipeline() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.9,
            stop_words="english",
            sublinear_tf=True,
        )),
        ("clf", LinearSVC(C=1.0, class_weight="balanced", random_state=42)),
    ])


def main():
    data_path = Path(__file__).parent / "synthetic_complaints.csv"
    texts, labels = load_data(str(data_path))

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.25, random_state=42, stratify=labels
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    print("=" * 60)
    print("CLASSIFICATION REPORT (held-out test set)")
    print("=" * 60)
    report = classification_report(y_test, y_pred, zero_division=0)
    print(report)

    labels_sorted = sorted(set(labels))
    cm = confusion_matrix(y_test, y_pred, labels=labels_sorted)
    print("Confusion matrix (rows = actual, cols = predicted):")
    print("Labels order:", labels_sorted)
    for row in cm:
        print(row)

    # Save model and report for reuse by the dashboard / demo script
    model_path = Path(__file__).parent / "complaint_classifier.joblib"
    joblib.dump(pipeline, model_path)
    print(f"\nModel saved to {model_path}")

    report_dict = classification_report(y_test, y_pred, zero_division=0, output_dict=True)
    metrics_path = Path(__file__).parent / "metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(report_dict, f, indent=2)
    print(f"Metrics saved to {metrics_path}")

    # A few live predictions on new, unseen example text to sanity check
    print("\n" + "=" * 60)
    print("SAMPLE PREDICTIONS ON NEW TEXT")
    print("=" * 60)
    samples = [
        "The bank charged me a fee on my credit card that was never disclosed when I signed up.",
        "My EMI for the personal loan was deducted twice this month without explanation.",
        "I cannot log into the mobile banking app and my UPI payment failed but money was deducted.",
        "The ATM did not give me cash but my account balance went down by five thousand rupees.",
    ]
    predictions = pipeline.predict(samples)
    for text, pred in zip(samples, predictions):
        print(f"\n  Text: {text}")
        print(f"  Predicted category: {pred}")


if __name__ == "__main__":
    main()
