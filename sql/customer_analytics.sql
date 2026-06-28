    -- customer distribution by country
    
select  country, count(distinct customer_id ) as customers
from fact_orders
group by country 
order by customers desc;

-- Top Spending Customers

select customer_id, round(sum(total_usd),2) as revenue 
from fact_orders
group by customer_id 
order by revenue desc;

-- Repeat customers

select count() as repeat_customer 
from (
select customer_id 
from fact_orders
group by customer_id
having count(order_id)>1);

-- customer segmentation 

with customer_revenue as (
select customer_id,
round(sum(total_usd),2) as revenue
from fact_orders
group by customer_id
),
customer_segment as 
(
select case 
            when revenue <=100 then 'Low Value '
            when revenue >100 and revenue<500 then 'Medium Value'
       else  'High Value'
       end as segment
from customer_revenue
)

select segment, count(*) as customers 
from customer_segment
group by segment 
order by customers desc;

-- Revenue by country
select country, count(customer_id) as customers, round(sum(total_usd),2) as revenue
from fact_orders
group by country 
order by revenue desc;

WITH customer_revenue AS (
    SELECT customer_id,
           ROUND(SUM(total_usd),2) AS revenue
    FROM fact_orders
    GROUP BY customer_id
),
customer_segment AS (
    SELECT revenue,
           CASE
             WHEN revenue <= 100 THEN 'Low Value'
             WHEN revenue < 500 THEN 'Medium Value'
             ELSE 'High Value'
           END AS segment
    FROM customer_revenue
)

SELECT segment,
       ROUND(SUM(revenue),2) AS total_revenue
FROM customer_segment
GROUP BY segment
ORDER BY total_revenue DESC;