import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠")

st.title("🏠 Customer Retention Dashboard")
st.subheader("客戶流失預警與留存管理系統")

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
## 📊 應用概述

這是一個**客戶流失預測與留存管理系統**，使用機器學習模型預測客戶流失風險，
並提供數據驅動的挽留策略建議。

### 🎯 核心功能

1. **Overview (總覽)** - 查看關鍵績效指標和客戶分布
2. **Data Snapshot (數據快照)** - 探索原始數據分布和特徵
3. **Model Comparison (模型對比)** - 比較不同機器學習模型的性能
4. **Customer Query (客戶查詢)** - 按客戶 ID 查詢流失風險和詳細信息
5. **Driver Analysis (驅動因子分析)** - 分析導致流失的主要特徵
6. **Retention Strategy (挽留策略)** - 根據風險和價值分級獲得策略建議
7. **Financial Impact (財務影響)** - 評估挽留活動的 ROI
8. **Governance (治理稽核)** - 審計日誌和人工覆核隊列

### 🤖 使用的模型

此應用訓練了 **4 個機器學習模型** 來預測客戶流失：

- **Logistic Regression** - 邏輯迴歸（基準模型）
- **Random Forest** - 隨機森林
- **XGBoost** - 梯度增強決策樹
- **LightGBM** - 生產環境部署模型（性能最優）

### 📈 主要指標

| 指標 | 描述 |
|------|------|
| **AUC** | 模型區分能力 (0.93+) |
| **Recall** | 識別流失客戶的能力 (62%+) |
| **Precision** | 預測準確度 |
| **F1 Score** | 精確度和召回率的調和平均 |

### 💡 快速開始

#### 首次使用（訓練模型）
```bash
python train.py
streamlit run app.py
```

#### 後續使用（使用已訓練的模型）
```bash
streamlit run app.py
```

### 📂 數據來源

- **訓練數據**: `data/抽樣後.csv` (30% 樣本)
- **儀表板數據**: `outputs/customer_scores.csv` (完整數據集)
- **模型檔案**: `models/` 目錄
- **輸出結果**: `outputs/` 目錄

### 🔑 關鍵欄位

| 欄位名稱 | 說明 |
|---------|------|
| `msno` | 客戶編號 |
| `是否流失` | 客戶是否流失 (0=留存, 1=流失) |
| `churn_score` | 流失概率評分 (0-1) |
| `risk_tier` | 風險分級 (Low/Medium/High) |
| `value_tier` | 價值分級 (Low Value/High Value) |

### 🎯 客群分級矩陣

系統根據 **風險等級** 和 **客戶價值** 將客戶分為以下幾類：

| 風險等級 | 高價值客戶 | 低價值客戶 |
|---------|----------|----------|
| **高風險** | 優先挽留 | 自動防禦 |
| **中等風險** | 忠誠培育 | 養成培育 |
| **低風險** | 高價值維護 | 常規推播 |

### 📊 推薦使用流程

1. **Overview** → 了解整體客群狀況
2. **Data Snapshot** → 探索數據特徵分布
3. **Model Comparison** → 理解各模型性能
4. **Driver Analysis** → 發現流失主要原因
5. **Customer Query** → 查詢個別客戶詳情
6. **Retention Strategy** → 制定挽留方案
7. **Financial Impact** → 評估投資回報
8. **Governance** → 審計和合規檢查

### ⚙️ 系統要求

- Python 3.9+
- Streamlit 1.35+
- scikit-learn, XGBoost, LightGBM
- Pandas, NumPy, Plotly

### 📞 數據說明

- **流失定義**: 訂閱已到期且未續約的客戶
- **目標客群**: 音樂串流平台用戶
- **數據週期**: 過去 6-12 個月
- **更新頻率**: 月度訓練

---

### 💡 使用提示

✅ **最佳實踐**：
- 定期檢查 Overview 掌握整體狀況
- 使用 Financial Impact 頁面進行成本效益分析
- 結合 Driver Analysis 理解業務洞察

⚠️ **注意事項**：
- 模型預測基於歷史數據，可能存在偏差
- 建議結合領域專家意見做最終決策
- 定期更新訓練數據以保持模型準確性
""")

with col2:
    st.markdown("""
### 📊 模型表現

**LightGBM (最優模型)**
- AUC: 0.9609 ✅
- Recall: 0.6312 ✅
- Precision: 0.55+
- F1: 0.59

**其他模型**
- XGBoost AUC: 0.9579
- Random Forest AUC: 0.9315
- Logistic Reg. AUC: 0.9368

### 📁 文件結構

```
├── app.py
├── train.py
├── config.py
├── requirements.txt
├── data/
│   └── 抽樣後.csv
├── models/
│   ├── lightgbm.pkl
│   ├── xgboost.pkl
│   ├── random_forest.pkl
│   ├── logistic_regression.pkl
│   └── model_metrics.json
├── outputs/
│   ├── customer_scores.csv
│   └── model_comparison.csv
├── utils/
│   ├── data_loader.py
│   ├── feature_engineering.py
│   ├── evaluation.py
│   ├── plotting.py
│   └── database.py
└── pages/
    ├── 01_Overview.py
    ├── 02_Data_Snapshot.py
    ├── 03_Model_Comparison.py
    ├── 04_Customer_Query.py
    ├── 05_Driver_Analysis.py
    ├── 06_Retention_Strategy.py
    ├── 07_Financial_Impact.py
    └── 08_Governance.py
```

### 🚀 快速命令

**訓練模型**
```bash
python train.py
```

**啟動應用**
```bash
streamlit run app.py
```

**清除緩存**
```bash
rm -rf .streamlit/
```

### 🔗 相關資源

- [Streamlit 文檔](https://docs.streamlit.io)
- [LightGBM 指南](https://lightgbm.readthedocs.io)
- [scikit-learn 文檔](https://scikit-learn.org)

""")

st.markdown("---")

st.info(
    "💡 **提示**: 使用左側導航菜單瀏覽各個分析頁面。"
    "首次使用請先執行 `python train.py` 訓練模型。"
)
