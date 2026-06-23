CREATE SCHEMA raw;
CREATE SCHEMA staging;
CREATE SCHEMA mart;

CREATE DATABASE airflow;
CREATE DATABASE superset;

CREATE TABLE IF NOT EXISTS raw.orders (
    order_id                VARCHAR PRIMARY KEY,
    customer_id             VARCHAR,
    order_status            VARCHAR,
    order_purchase_timestamp TIMESTAMP,
    order_approved_at       TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date DATE
);

CREATE TABLE IF NOT EXISTS raw.order_items (
    order_id        VARCHAR,
    order_item_id   INTEGER,
    product_id      VARCHAR,
    seller_id       VARCHAR,
    shipping_limit_date TIMESTAMP,
    price           NUMERIC,
    freight_value   NUMERIC
);