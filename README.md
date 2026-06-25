# 🛒 End-to-End E-Commerce Data Engineering Project

## 📌 Project Overview
This repository contains a complete **End-to-End Data Engineering Pipeline (ETL)**. The project extracts raw Brazilian E-Commerce (Olist) data using Python, transforms and cleans it, and loads it into a PostgreSQL Data Warehouse. Finally, advanced SQL analytical queries were executed to build an interactive business dashboard in Power BI.

## 🛠️ Tech Stack Used
- **Programming Language:** Python (Pandas, SQLAlchemy)
- **Database / Data Warehouse:** PostgreSQL (pgAdmin 4)
- **Business Intelligence Tool:** Power BI Desktop

## 🚀 Pipeline Architecture & Steps
1. **Data Extraction:** Raw transactional datasets in CSV format were extracted using the Python `pandas` library.
2. **Data Transformation:** Performed data cleaning, handled missing records, and resolved strict data type mismatches (e.g., casting text fields into clean `timestamp` formats).
3. **Data Loading:** Established a secure connection using `SQLAlchemy` to automatically push and build schema tables inside the `ecommerce_dw` database.

## 📊 Advanced SQL Analytics (Interview-Level)
To derive deep business insights, the following production-grade SQL concepts were implemented:
- **Month-over-Month (MoM) Growth:** Utilized the `LAG()` window function combined with `GENERATE_SERIES()` to handle missing time series data (Gap Filling).
- **Customer Cohort Analysis:** Implemented `MIN()` and `AGE()` window functions to calculate and analyze customer retention rates over time.
- **Running Total (Cumulative Sum):** Designed a `SUM() OVER (ORDER BY...)` analytical query to track month-on-month business growth.

## 📈 Power BI Dashboard Insights
- **Cumulative Order Growth:** The line chart effectively communicates the continuous upward trend of total orders processed by the platform.
- **Data-Driven Strategy:** This analytical dashboard enables stakeholders to quickly pinpoint seasonal sales drops and monitor business health in real-time.
