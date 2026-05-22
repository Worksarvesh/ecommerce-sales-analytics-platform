DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY,
    country VARCHAR(100) NOT NULL
);

CREATE TABLE products (
    stock_code VARCHAR(20) PRIMARY KEY,
    description TEXT NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price > 0)
);

CREATE TABLE orders (
    invoice_no VARCHAR(20) NOT NULL,
    customer_id BIGINT NOT NULL REFERENCES customers(customer_id),
    stock_code VARCHAR(20) NOT NULL REFERENCES products(stock_code),
    quantity INT NOT NULL CHECK (quantity > 0),
    invoice_date TIMESTAMP NOT NULL,
    total_revenue NUMERIC(12,2) NOT NULL CHECK (total_revenue >= 0),
    PRIMARY KEY (invoice_no, stock_code)
);

CREATE INDEX idx_orders_invoice_date ON orders(invoice_date);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_stock_code ON orders(stock_code);
CREATE INDEX idx_customers_country ON customers(country);
CREATE INDEX idx_orders_revenue_desc ON orders(total_revenue DESC);
