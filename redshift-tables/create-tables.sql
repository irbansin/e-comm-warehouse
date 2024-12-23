CREATE TABLE sales_fact (
    sales_id BIGINT IDENTITY(1, 1),
    customer_id INT,
    product_id INT,
    seller_id INT,
    category_id INT,
    time_id DATE,
    price NUMERIC(18, 2),
    freight_value NUMERIC(18, 2),
    payment_value NUMERIC(18, 2),
    PRIMARY KEY (sales_id)
);

CREATE TABLE customers_dim (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(255),
    customer_city VARCHAR(100),
    customer_state VARCHAR(100)
);

CREATE TABLE products_dim (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    product_category VARCHAR(100)
);

CREATE TABLE sellers_dim (
    seller_id INT PRIMARY KEY,
    seller_name VARCHAR(255),
    seller_city VARCHAR(100),
    seller_state VARCHAR(100)
);

CREATE TABLE categories_dim (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100)
);

CREATE TABLE time_dim (
    time_id DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT
);
