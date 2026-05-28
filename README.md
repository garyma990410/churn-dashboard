# Customer Retention Dashboard
## 客戶洞察與留存管理系統

### Quick Start
```bash
pip install -r requirements.txt

# 1. Place your CSVs in data/
#    data/抽樣後.csv   (30% sample → training)
#    data/full_data.csv  (full ~970k rows → dashboard display)

# 2. Train models
python train.py

# 3. Launch dashboard
streamlit run app.py
```

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