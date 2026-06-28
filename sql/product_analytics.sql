-- products generate the highest revenue?

select dp.product_id, dp.name, round(sum(fo.line_total_usd),2) as revenue
from dim_products dp 
join fact_order_items fo 
on dp.product_id=fo.product_id 
group by dp.product_id, dp.name
order by revenue desc
limit 10;

-- best selling products by quantity

select dp.name, sum(fo.quantity) as quantity
from dim_products dp 
join fact_order_items fo 
on dp.product_id=fo.product_id
group by dp.name, quantity
order by quantity desc
limit 10;

-- Category Performance

select dp.category, round(sum(fo.line_total_usd),2) as revenue 
from dim_products dp 
join fact_order_items fo 
on dp.product_id=fo.product_id
group by dp.category
order by revenue desc;

-- category contribution_pct

with category_revenue as (
select dp.category, round(sum(fo.line_total_usd),2) as revenue 
from dim_products dp 
join fact_order_items fo 
on dp.product_id=fo.product_id
group by dp.category

)

select category,
round(revenue,2) as revenue,
round(100*revenue/sum(revenue) over(),2) as contribution_pct
from category_revenue
order by contribution_pct desc;
