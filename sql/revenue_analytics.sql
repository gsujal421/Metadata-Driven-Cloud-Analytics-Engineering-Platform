-- Revenue analytics
-- total revenue

select round(sum(line_total_usd),2) as total_revenue
from fact_order_items;

-- average order value 

select 
round(sum(total_usd),2) as revenue,
count(order_id) as total_ordes,
round(sum(total_usd)/(count(order_id)),2) as average_order
from fact_orders;

-- revenue by country

select 
distinct(country),
round(sum(total_usd),2) as revenue
from fact_orders
group by country
order by revenue desc;

-- revenue by source

select 
distinct(source),
round(sum(total_usd),2) as revenue
from fact_orders
group by source
order by revenue desc;

SELECT
    source,
    COUNT(order_id) AS orders,
    ROUND(SUM(total_usd),2) AS revenue,
    ROUND(SUM(total_usd)/COUNT(order_id),2) AS avg_order_value
FROM fact_orders
GROUP BY source 
ORDER BY revenue DESC;