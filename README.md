# Store Sales Data Cleaning & Time-Series Analysis Pipeline

An automated, end-to-end data engineering and analytics pipeline built with **Python** and **Pandas** to sanitize messy retail sales data, resolve temporal gaps, handle statistical outliers, and compute accurate rolling window metrics for business forecasting.

---

## Business Problem
Raw point-of-sale (POS) data in retail environments frequently suffers from inconsistent date formatting, missing daily records, and extreme data entry errors. Feeding uncleaned data directly into business intelligence dashboards or forecasting models distorts revenue trends, misleads inventory planning, and produces inaccurate moving averages. 

This project provides a reproducible data cleaning pipeline that transforms corrupted raw sales logs into reliable, analysis-ready time-series datasets.

---

##  Key Features & Methodology

1. **Date Standardization & Gap Filling**
   * Parses mixed date formats into a unified `datetime64` index.
   * Reindexes the dataset against a continuous calendar range (`pd.date_range`) to expose and fill hidden missing dates (temporal gaps).

2. **Outlier Detection & Treatment**
   * Identifies extreme anomalies caused by manual entry errors (e.g., extra zeros or negative values) using the **Interquartile Range (IQR)** method.
   * Caps or replaces anomalous records with context-aware statistical thresholds to preserve overall distribution integrity.

3. **Missing Value Imputation**
   * Handles missing sales figures using time-aware **linear interpolation** (`interpolate(method='time')`), ensuring continuity without introducing artificial spikes.

4. **Rolling Window Analytics**
   * Computes **7-day** and **30-day Rolling Averages** (`rolling(window=7).mean()`) on the sanitized time series to smooth out daily volatility and reveal true underlying sales trends.

---

##  Project Structure

```text
store-sales-cleaning-pipeline/
├── data/
│   ├── raw_sales.csv               # Sample raw dataset containing dates/values anomalies
│   └── cleaned_sales.csv           # Sanitized output dataset with rolling metrics
├── notebooks/
│   └── analysis_walkthrough.ipynb  # Step-by-step EDA, cleaning logic, and visualizations
├── src/
│   └── pipeline.py                 # Modular, production-ready Python cleaning script
├── assets/
│   └── before_after_comparison.png # Visual comparison of raw vs. cleaned sales trends
├── requirements.txt                # Project dependencies
└── README.md                       # Project documentation
