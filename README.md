# E-Commerce Sales Analytics Platform

A complete production-quality analytics project using Flask, PostgreSQL, pandas, SQL, Bootstrap, and Chart.js. The platform downloads the Kaggle `carrie1/ecommerce-data` dataset, cleans it, loads a normalized PostgreSQL schema, exposes analytics APIs, renders a professional dashboard, and provides a Power BI-compatible CSV export.

## Screenshots

Add screenshots after running locally:

- `screenshots/home.png`
- `screenshots/dashboard.png`
- `screenshots/powerbi-export.png`

## Tech Stack

- Backend: Python 3.11+, Flask, PostgreSQL, psycopg2-binary, SQLAlchemy, pandas, python-dotenv
- Frontend: HTML, CSS, JavaScript, Bootstrap, Chart.js
- Dataset: Kaggle `carrie1/ecommerce-data`
- BI Export: CSV endpoint for Power BI import

## Project Structure

```text
ecommerce-analytics/
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── README.md
├── database.sql
├── queries.sql
├── data/
├── scripts/
│   ├── download_dataset.py
│   ├── clean_data.py
│   ├── load_data.py
│   ├── db_connection.py
│   └── analytics.py
├── templates/
│   ├── index.html
│   └── dashboard.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── dashboard.js
```

## Dataset Columns

The project uses only the actual Kaggle dataset columns:

- `InvoiceNo`
- `StockCode`
- `Description`
- `Quantity`
- `InvoiceDate`
- `UnitPrice`
- `CustomerID`
- `Country`

Derived column:

- `TotalRevenue = Quantity * UnitPrice`

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your environment file:

```bash
copy .env.example .env
```

Update `.env` with your PostgreSQL credentials.

## PostgreSQL Setup

Create the database:

```sql
CREATE DATABASE ecommerce_analytics;
```

The loader can create the schema automatically from `database.sql`. To run it manually:

```bash
psql -U postgres -d ecommerce_analytics -f database.sql
```

## Data Pipeline

Download the Kaggle dataset:

```bash
python scripts/download_dataset.py
```

Clean the data:

```bash
python scripts/clean_data.py
```

Load the data into PostgreSQL:

```bash
python scripts/load_data.py
```

The cleaning pipeline removes rows with null `CustomerID`, cancelled invoices, duplicate rows, negative or zero quantities, zero prices, invalid dates, and creates `TotalRevenue`.

## Run Flask

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

Dashboard:

```text
http://localhost:5000/dashboard
```

## API Documentation

### Total Sales

`GET /api/total-sales`

```json
{
  "total_revenue": 8911407.9
}
```

### Monthly Sales

`GET /api/monthly-sales`

```json
[
  {
    "month": "2010-12",
    "revenue": 572713.89
  }
]
```

### Top Products

`GET /api/top-products`

Returns the top 10 products by units sold.

### Country Sales

`GET /api/country-sales`

Returns revenue grouped by country.

### Best Customers

`GET /api/best-customers`

Returns the top 10 customers by revenue.

### Average Order Value

`GET /api/average-order-value`

Returns the average invoice value.

### Customer Ranking

`GET /api/customer-ranking`

Returns customers ranked by revenue using a SQL window function.

### Power BI CSV Export

`GET /api/export-csv`

Downloads a flattened CSV containing invoice, customer, country, product, quantity, date, unit price, and revenue fields.

## SQL Analytics

The main analytics queries are stored in `queries.sql` and implemented in `scripts/analytics.py`:

- Total revenue
- Monthly sales trend
- Top selling products
- Country revenue
- Best customers
- Average order value
- Customer ranking with `RANK()`

## Database Design

### customers

- `customer_id BIGINT PRIMARY KEY`
- `country VARCHAR(100)`

### products

- `stock_code VARCHAR(20) PRIMARY KEY`
- `description TEXT`
- `unit_price NUMERIC(10,2)`

### orders

- `invoice_no VARCHAR(20)`
- `customer_id BIGINT REFERENCES customers(customer_id)`
- `stock_code VARCHAR(20) REFERENCES products(stock_code)`
- `quantity INT`
- `invoice_date TIMESTAMP`
- `total_revenue NUMERIC(12,2)`
- Primary key: `(invoice_no, stock_code)`

## Power BI Integration

Use Power BI Desktop:

1. Select **Get Data**.
2. Choose **Web**.
3. Enter `http://localhost:5000/api/export-csv`.
4. Load or transform the CSV.
5. Build visuals using `invoice_date`, `country`, `description`, `quantity`, and `total_revenue`.

For scheduled refresh in production, deploy the Flask app behind HTTPS and use the hosted `/api/export-csv` URL.

## Resume Bullet Points

- Built a full-stack E-Commerce Sales Analytics Platform using Flask, PostgreSQL, pandas, SQL, Bootstrap, and Chart.js.
- Automated Kaggle dataset download, data cleaning, revenue derivation, and normalized PostgreSQL loading.
- Designed analytics-ready relational tables with indexes for revenue, product, customer, and country analysis.
- Implemented REST APIs for KPI metrics, monthly trends, top products, country revenue, customer rankings, and Power BI CSV export.
- Created a responsive executive dashboard with KPI cards, line charts, bar charts, pie charts, loading states, and error handling.
- Used SQL window functions and aggregate queries to support portfolio-grade business intelligence use cases.

## Production Notes

- Store real credentials in `.env`, never in source control.
- Use `gunicorn` or a WSGI server for deployment.
- Put Flask behind Nginx or a managed platform reverse proxy.
- Use managed PostgreSQL for cloud deployment.
- Add authentication before exposing internal analytics dashboards publicly.
