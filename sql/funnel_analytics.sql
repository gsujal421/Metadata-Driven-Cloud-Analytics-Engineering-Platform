-- funnel stages

select distinct event_type
from fact_events;

-- unique sessions in each event

select event_type,
count(distinct(session_id)) as sessions
from fact_events
group by event_type
order by sessions desc;

-- where customer drop off

with funnel as (
select CASE
    WHEN event_type='page_view' THEN 1
    WHEN event_type='add_to_cart' THEN 2
    WHEN event_type='checkout' THEN 3
    WHEN event_type='purchase' THEN 4
END AS stage_order,
       event_type,
       count(distinct(session_id)) as sessions
       from fact_events
       where event_type in (
       'page_view',
        'add_to_cart',
        'checkout',
        'purchase'
       )
        
       group by  event_type
       
)

select event_type,sessions
ROUND(100.0 * sessions / LAG(sessions) OVER (ORDER BY stage_order), 2)
from funnel
order by stage_order;

SELECT
    fs.device,

    COUNT(
        DISTINCT CASE
            WHEN fe.event_type = 'purchase'
            THEN fe.session_id
        END
    ) AS purchasing_sessions,

    COUNT(
        DISTINCT fe.session_id
    ) AS total_sessions,

    ROUND(
        100.0 *
        COUNT(
            DISTINCT CASE
                WHEN fe.event_type = 'purchase'
                THEN fe.session_id
            END
        )
        /
        COUNT(DISTINCT fe.session_id),
        2
    ) AS conversion_pct

FROM fact_events fe
JOIN fact_sessions fs
    ON fe.session_id = fs.session_id

GROUP BY fs.device
ORDER BY conversion_pct DESC;

