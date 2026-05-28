import pandas as pd
from config import SAMPLE_CSV, FULL_CSV, LABEL_COL, MSNO_COL, FEATURE_COLS, TRAIN_SAMPLE_FRAC, RANDOM_STATE

def load_sample() -> pd.DataFrame:
    df = pd.read_csv(SAMPLE_CSV, encoding='big5')
    return df

def load_full() -> pd.DataFrame:
    try:
        df = pd.read_csv(FULL_CSV, encoding='big5')
    except FileNotFoundError:
        df = pd.read_csv(SAMPLE_CSV, encoding='big5')
    return df

def get_X_y(df: pd.DataFrame):
    X = df[FEATURE_COLS].copy()
    y = df[LABEL_COL].copy()
    return X, y