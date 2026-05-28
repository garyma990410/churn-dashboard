"""
train.py
Run this once before launching the dashboard.
  python train.py
"""
import json, pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from config import (
    SAMPLE_CSV, LABEL_COL, FEATURE_COLS,
    TEST_SIZE, RANDOM_STATE, MODEL_DIR, OUTPUT_DIR
)
from utils.data_loader import load_sample, get_X_y
from utils.feature_engineering import add_features
from utils.evaluation import evaluate, metrics_table

def main():
    print("Loading sample CSV …")
    df = load_sample()
    df = add_features(df)

    FEATS = FEATURE_COLS + ["high_cancel_risk", "activity_ratio", "payment_low"]
    X = df[FEATS]
    y = df[LABEL_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE
    )
    print(f"Train: {len(X_train)}  Test: {len(X_test)}  Churn rate: {y.mean():.2%}")

    models = {
        "Logistic Regression": LogisticRegression(max_iter=500, random_state=RANDOM_STATE),
        "Random Forest":       RandomForestClassifier(n_estimators=200, n_jobs=-1, random_state=RANDOM_STATE),
        "XGBoost":             XGBClassifier(n_estimators=300, use_label_encoder=False,
                                             eval_metric="logloss", random_state=RANDOM_STATE),
        "LightGBM":            LGBMClassifier(n_estimators=300, random_state=RANDOM_STATE, verbose=-1),
    }

    results = {}
    for name, clf in models.items():
        print(f"Training {name} …")
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1]
        results[name] = evaluate(y_test, y_pred, y_prob)
        pkl_path = MODEL_DIR + name.lower().replace(" ", "_") + ".pkl"
        with open(pkl_path, "wb") as f:
            pickle.dump(clf, f)
        print(f"  AUC={results[name]['AUC']}  Recall={results[name]['Recall']}")

    metrics_table(results).to_csv(OUTPUT_DIR + "model_comparison.csv")
    with open(MODEL_DIR + "model_metrics.json", "w") as f:
        json.dump(results, f, indent=2)

    # Generate customer scores using best model (LightGBM)
    lgb = models["LightGBM"]
    df_full = pd.read_csv(SAMPLE_CSV, encoding='big5')
    df_full = add_features(df_full)
    df_full["churn_score"] = lgb.predict_proba(df_full[FEATS])[:, 1]
    df_full["risk_tier"]   = pd.cut(df_full["churn_score"],
                                    bins=[-0.001, 0.20, 0.50, 1.001],
                                    labels=["Low", "Medium", "High"])
    df_full["value_tier"]  = pd.cut(df_full["近兩個月付費次數"],
                                    bins=[-1, 1, 999],
                                    labels=["Low Value", "High Value"])
    df_full.to_csv(OUTPUT_DIR + "customer_scores.csv", index=False)
    print("\nDone! Artifacts saved to models/ and outputs/")

if __name__ == "__main__":
    main()