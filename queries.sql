-- 1. Total Revenue
SELECT SUM(total_revenue)
FROM orders;

-- 2. Monthly Sales Trend
SELECT
    DATE_TRUNC('month', invoice_date) AS month,
    SUM(total_revenue)
FROM orders
GROUP BY month
ORDER BY month;

-- 3. Top Selling Products
SELECT
    p.description,
    SUM(o.quantity) total_sold
FROM orders o
JOIN products p
ON o.stock_code = p.stock_code
GROUP BY p.description
ORDER BY total_sold DESC
LIMIT 10;

-- 4. Country Revenue
SELECT
    c.country,
    SUM(o.total_revenue) revenue
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
GROUP BY c.country
ORDER BY revenue DESC;

-- 5. Best Customers
SELECT
    customer_id,
    SUM(total_revenue) revenue
FROM orders
GROUP BY customer_id
ORDER BY revenue DESC
LIMIT 10;

-- 6. Average Order Value
SELECT AVG(order_total)
FROM (
    SELECT invoice_no, SUM(total_revenue) order_total
    FROM orders
    GROUP BY invoice_no
) x;

-- 7. Customer Ranking (window function)
SELECT
    customer_id,
    SUM(total_revenue),
    RANK() OVER (ORDER BY SUM(total_revenue) DESC)
FROM orders
GROUP BY customer_id;
