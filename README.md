# Customer Retention Dashboard
## 客戶洞察與留存管理系統

### Quick Start

#### 使用預訓練模型（推薦）
```bash
pip install -r requirements.txt

# 直接啟動儀表板（使用已訓練的模型）
streamlit run app.py
```

#### 從頭訓練新模型
```bash
pip install -r requirements.txt

# 1. 將資料放在 data/ 目錄
#    data/抽樣後.csv   (30% sample → training)
#    data/full_data.csv  (full ~970k rows → dashboard display)

# 2. 訓練模型（第一次或更新資料時執行）
python train.py

# 3. 啟動儀表板
streamlit run app.py
```

**訓練完成後的文件：**
- `models/logistic_regression.pkl` - Logistic Regression 模型
- `models/random_forest.pkl` - Random Forest 模型
- `models/xgboost.pkl` - XGBoost 模型
- `models/lightgbm.pkl` - LightGBM 模型（生產環境使用）
- `outputs/customer_scores.csv` - 所有客戶的流失評分和風險分級
- `outputs/model_comparison.csv` - 模型評估指標對比
- `models/model_metrics.json` - 詳細的模型性能指標

### Deploying to Streamlit Community Cloud
1. Push this folder to a public GitHub repository.
2. Go to https://share.streamlit.io → New app.
3. Select your repo, branch, and `app.py` as the entry file.
4. Add `data/抽樣後.csv` to the repo (or use Git LFS for large files).
5. Click Deploy.

### Page Structure
| Page | Content |
|---|---|
| Overview | KPI cards + 5 donuts |
| Data Snapshot | Distribution charts + raw preview |
| Model Comparison | LR / RF / XGBoost / LightGBM metrics |
| Customer Query | Search by msno, risk gauge, profile |
| Driver Analysis | Feature importance + correlation |
| Retention Strategy | 4-segment strategy cards |
| Financial Impact | ROI waterfall + scenario sliders |
| Governance | Audit log + manual review queue |

### Models Used
- Baseline: Logistic Regression
- Advanced: Random Forest, XGBoost, LightGBM
- Deployment: LightGBM
- Metrics: AUC, Recall, Precision, F1

### Data
- Training: 30% sample of cleaned CSV (cutoff already applied)
- Dashboard display: full ~970k rows CSV
- Target: `是否流失` (1 = churned, 0 = retained)