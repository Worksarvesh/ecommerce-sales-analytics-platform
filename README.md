# 🛒 E-Commerce Sales Analytics Platform

A full-stack data analytics platform built to transform raw e-commerce transactional data into actionable business insights through advanced SQL analytics, backend APIs, and interactive dashboard visualizations.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-Backend-black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-purple)
![Chart.js](https://img.shields.io/badge/Chart.js-Visualization-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Live Demo
🔗 **Live Project:** https://your-live-link.com

## 💻 GitHub Repository
🔗 **Source Code:** https://github.com/Worksarvesh/ecommerce-analytics

---

## 📌 Project Overview

This project is a full-stack analytics dashboard designed to analyze e-commerce sales transactions and provide business intelligence insights.

The platform processes raw transactional data, cleans and transforms it, stores it in PostgreSQL, runs advanced SQL analytics queries, exposes REST APIs via Flask, and visualizes insights through an interactive dashboard.

It simulates a real-world analytics workflow commonly used in data analyst and backend engineering roles.

---

## ✨ Features

### Business Analytics
- 📈 Total Revenue Analysis
- 📊 Monthly Sales Trend Visualization
- 🏆 Top Selling Products Analysis
- 🌍 Country-wise Revenue Performance
- 👥 Customer Revenue Ranking
- 💰 Average Order Value Calculation
- 📦 Product Performance Metrics

### Backend Engineering
- RESTful API endpoints
- Flask backend architecture
- PostgreSQL database integration
- SQL query optimization
- Modular project structure
- CSV export functionality

### Data Engineering Workflow
- Dataset ingestion automation
- Data cleaning pipeline
- Duplicate handling
- Missing value handling
- Transaction filtering
- Revenue transformation logic

### Dashboard UI
- Interactive KPI cards
- Dynamic line charts
- Product performance bar charts
- Country revenue donut chart
- Customer ranking tables
- Responsive dashboard interface

---

## 🏗 Tech Stack

### Backend
- Python
- Flask
- PostgreSQL
- SQLAlchemy
- psycopg2

### Data Processing
- Pandas
- NumPy

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap
- Chart.js

### Tools
- VS Code
- pgAdmin
- Git
- GitHub

---

## 📂 Project Architecture

```bash
ecommerce-analytics/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .env.example
├── database.sql
├── queries.sql
├── README.md
│
├── data/
│   └── cleaned_ecommerce.csv
│
├── scripts/
│   ├── analytics.py
│   ├── clean_data.py
│   ├── db_connection.py
│   ├── download_dataset.py
│   └── load_data.py
│
├── templates/
│   ├── index.html
│   └── dashboard.html
│
├── static/
│   ├── css/
│   └── js/
```

---

## 🗄 Database Design

### Customers Table
| Column | Type |
|------|------|
| customer_id | BIGINT |
| country | VARCHAR |

### Products Table
| Column | Type |
|------|------|
| stock_code | VARCHAR |
| description | TEXT |
| unit_price | NUMERIC |

### Orders Table
| Column | Type |
|------|------|
| invoice_no | VARCHAR |
| customer_id | BIGINT |
| stock_code | VARCHAR |
| quantity | INT |
| invoice_date | TIMESTAMP |
| total_revenue | NUMERIC |

---

## 📊 Analytics Implemented

### Revenue Metrics
- Total Revenue
- Average Order Value
- Monthly Revenue Trends

### Product Analytics
- Top Selling Products
- Product Unit Performance

### Customer Analytics
- Customer Revenue Ranking
- Top Customer Identification

### Geographic Analytics
- Country Revenue Distribution
- Top Market Performance

---

## 🧠 Advanced SQL Concepts Used

This project includes practical implementation of:

- INNER JOIN
- GROUP BY
- ORDER BY
- Aggregation Functions
- Common Table Expressions (CTEs)
- Window Functions
- RANK()
- DATE_TRUNC()
- Subqueries
- Revenue Calculations
- Data Filtering

Example:

```sql
SELECT
    customer_id,
    SUM(total_revenue),
    RANK() OVER (ORDER BY SUM(total_revenue) DESC)
FROM orders
GROUP BY customer_id;
```

---

## 🔌 API Endpoints

| Endpoint | Description |
|--------|-------------|
| /api/total-sales | Fetch total revenue |
| /api/monthly-sales | Monthly sales trend |
| /api/top-products | Top selling products |
| /api/country-sales | Country-wise revenue |
| /api/best-customers | Best customers ranking |
| /api/average-order-value | Average order value |
| /api/customer-ranking | Customer performance |

---

## 📥 Dataset Information

Dataset Source:
**Kaggle - E-Commerce Data**

Dataset columns:
- InvoiceNo
- StockCode
- Description
- Quantity
- InvoiceDate
- UnitPrice
- CustomerID
- Country

Cleaning performed:
- Removed null customer records
- Removed cancelled transactions
- Removed duplicate rows
- Removed negative quantities
- Removed invalid prices
- Added derived revenue column

---

## ⚙ Installation Guide

### 1. Clone repository

```bash
git clone https://github.com/Worksarvesh/ecommerce-analytics.git
cd ecommerce-analytics
```

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate:

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Setup PostgreSQL

Create database:

```sql
CREATE DATABASE ecommerce_analytics;
```

Run schema:

```bash
database.sql
```

---

### 5. Configure environment variables

Create `.env`

```env
DB_HOST=localhost
DB_NAME=ecommerce_analytics
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_PORT=5432
```

---

### 6. Download and clean dataset

```bash
python scripts/download_dataset.py
python scripts/clean_data.py
```

---

### 7. Load data into PostgreSQL

```bash
python scripts/load_data.py
```

---

### 8. Run application

```bash
python app.py
```

Open browser:

```bash
http://127.0.0.1:5000
```

---

## 📷 Screenshots

Add screenshots here:

```markdown
![Dashboard](screenshots/dashboard.png)
```

---

## 🎯 Resume Highlights

This project demonstrates:

- Full-stack application development
- SQL analytics engineering
- PostgreSQL database design
- Data cleaning & transformation
- REST API backend development
- Business intelligence dashboard creation
- Real-world data analysis workflow

---

## 🔮 Future Enhancements

Planned upgrades:

- Date range filtering
- Product search
- Country filtering
- Authentication
- User login dashboard
- Export to Excel
- Power BI direct integration
- Predictive sales forecasting

---

## 👨‍💻 Author

**Sarvesh Sharma**

📧 worksarvesh05@gmail.com  
🔗 LinkedIn: https://www.linkedin.com/in/sarvesh-sharma-432738354/  
💻 GitHub: https://github.com/Worksarvesh

---

## ⭐ If you found this useful

Star the repository ⭐
