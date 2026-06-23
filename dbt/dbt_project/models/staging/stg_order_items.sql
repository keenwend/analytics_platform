{{ config(materialized='table') }}

with source as (
    select * from raw.order_items
)
select
    order_id,
    order_item_id,
    product_id,
    seller_id,
    shipping_limit_date::timestamp as shipping_limit_date,
    price::numeric        as price,
    freight_value::numeric as freight_value,
    price + freight_value  as total_value
from source
