{{ config(
    materialized='table'
    ) }}

select
    date_trunc('day', o.purchased_at)::date as order_date,
    o.order_status,
    count(distinct o.order_id)              as orders_count,
    count(i.order_item_id)                  as items_count,
    round(sum(i.price)::numeric, 2)         as revenue,
    round(sum(i.freight_value)::numeric, 2) as freight_total,
    round(sum(i.total_value)::numeric, 2)   as gmv
from {{ ref('stg_orders') }} o
left join {{ ref('stg_order_items') }} i using (order_id)
group by 1, 2
order by 1 desc