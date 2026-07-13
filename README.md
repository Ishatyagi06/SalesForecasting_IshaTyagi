
# 📊 Sales Forecasting & Demand Intelligence System

## 🚀 Overview

The **Sales Forecasting & Demand Intelligence System** is a machine learning-based retail analytics solution that helps businesses predict future sales, understand demand patterns, detect unusual sales behavior, and improve inventory planning.

The project provides an interactive **Streamlit dashboard** for analyzing sales trends, product performance, anomalies, and product segments.

---

## 🎯 Objectives

- Analyze historical sales trends
- Forecast future sales demand
- Detect unusual sales patterns
- Segment products based on performance
- Support better inventory decisions

---

## 📌 Dashboard Features

### 📊 Sales Analysis
- Sales trends over time
- Category and product performance
- Revenue insights

### ⚠️ Anomaly Detection
- Identifies unusual sales patterns using Isolation Forest
- Highlights possible reasons like promotions, seasonal demand, or supply issues

### 📦 Product Segmentation
- Classifies products into:
  - High Value
  - Medium Value
  - Low Value

Helps optimize stocking strategies.

---

## 🛠️ Tech Stack

- **Python**
- **Pandas & NumPy**
- **Scikit-learn**
- **Plotly**
- **Streamlit**
- **Matplotlib & Seaborn**

---

## 📂 Project Structure


SalesForecasting_Project/
│
├── app.py
├── requirements.txt
├── README.md
├── data/
│ └── sales_data.csv
└── models/
└── forecasting_model.pkl

---

## ⚙️ Run Locally

Install dependencies:

```bash
pip install -r requirements.txt

streamlit run app.py
