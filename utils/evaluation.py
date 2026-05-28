from sklearn.metrics import (
    roc_auc_score, recall_score, precision_score,
    f1_score, confusion_matrix, classification_report
)
import pandas as pd

def evaluate(y_true, y_pred, y_prob) -> dict:
    return {
        "AUC":       round(roc_auc_score(y_true, y_prob), 4),
        "Recall":    round(recall_score(y_true, y_pred),   4),
        "Precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "F1":        round(f1_score(y_true, y_pred),       4),
    }

def metrics_table(results: dict) -> pd.DataFrame:
    rows = []
    for model, m in results.items():
        rows.append({"Model": model, **m})
    return pd.DataFrame(rows).set_index("Model")