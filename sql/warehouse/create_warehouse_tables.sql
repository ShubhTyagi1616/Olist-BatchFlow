-- create warehouse schema (STAR SCHEMA) for warehouse tables : 

CREATE TABLE warehouse.dim_customers (
    customer_id VARCHAR PRIMARY KEY,
    customer_unique_id VARCHAR,
    customer_city VARCHAR,
    customer_state VARCHAR
);


CREATE TABLE warehouse.dim_sellers (
    seller_id VARCHAR PRIMARY KEY,
    seller_city VARCHAR,
    seller_state VARCHAR
);


CREATE TABLE warehouse.dim_products (
    product_id VARCHAR PRIMARY KEY,
    product_category_english VARCHAR,
    product_weight_g NUMERIC,
    product_length_cm NUMERIC,
    product_height_cm NUMERIC,
    product_width_cm NUMERIC
);

CREATE TABLE warehouse.dim_date (
    date_id DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT,
    weekday VARCHAR
);


CREATE TABLE warehouse.fact_orders (
    order_id VARCHAR,
    order_item_id INT,
    customer_id VARCHAR REFERENCES warehouse.dim_customers(customer_id),
    seller_id VARCHAR REFERENCES warehouse.dim_sellers(seller_id),
    product_id VARCHAR REFERENCES warehouse.dim_products(product_id),
    order_purchase_date DATE REFERENCES warehouse.dim_date(date_id),
    order_status VARCHAR,
    price NUMERIC,
    freight_value NUMERIC,
    payment_value NUMERIC,
    review_score INT
);