LABEL_COL    = "是否流失"
MSNO_COL     = "msno"
FEATURE_COLS = [
    "會員年資天數", "年齡", "是否自動續約",
    "近一次交易是否取消", "近兩個月付費次數", "近一個月活躍天數"
]
TRAIN_SAMPLE_FRAC = 0.30        # train on 30% sample
RANDOM_STATE      = 42
TEST_SIZE         = 0.20
HIGH_RISK_THRESH  = 0.20        # top 20% = high-risk
CHURN_THRESHOLD   = 0.50        # binary cutoff for label

# CSV paths (relative to project root)
SAMPLE_CSV   = "data/抽樣後.csv"      # 30% sample → training
FULL_CSV     = "data/full_data.csv"   # ~970k rows → dashboard display

MODEL_DIR    = "models/"
OUTPUT_DIR   = "outputs/"

# Retention assumptions (default, overridable via UI sliders)
DEFAULT_MONTHLY_REVENUE = 10.0      # USD per customer
DEFAULT_EXTENSION_MONTHS = 6
DEFAULT_SUCCESS_RATE = 0.15
DEFAULT_OUTREACH_COST = 4.5