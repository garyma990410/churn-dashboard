import pandas as pd

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["high_cancel_risk"]   = ((df["近一次交易是否取消"] == 1) & (df["是否自動續約"] == 0)).astype(int)
    df["activity_ratio"]     = df["近一個月活躍天數"] / 31.0
    df["payment_low"]        = (df["近兩個月付費次數"] <= 1).astype(int)
    df["tenure_bucket"]      = pd.cut(df["會員年資天數"],
                                      bins=[-1, 180, 365, 730, 9999],
                                      labels=["<6m", "6-12m", "1-2y", "2y+"])
    return df