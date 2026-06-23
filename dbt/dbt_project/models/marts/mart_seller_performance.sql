{{ config(
    materialized='table'
    ) }}

select
    i.seller_id,
    count(distinct o.order_id)          as total_orders,
    count(i.order_item_id)              as total_items,
    round(sum(i.price)::numeric, 2)     as total_revenue,
    round(avg(i.price)::numeric, 2)     as avg_item_price,
    min(o.purchased_at)::date           as first_sale_date,
    max(o.purchased_at)::date           as last_sale_date
from {{ ref('stg_order_items') }} i
join {{ ref('stg_orders') }} o using (order_id)
where o.order_status = 'delivered'
group by 1
order by total_revenue desc