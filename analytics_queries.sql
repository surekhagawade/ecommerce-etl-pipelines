-------------------------------------------------------------------
-- Challenge 1: Month-over-Month (MoM) Order Growth % (With Gap Filling)
-------------------------------------------------------------------
WITH date_bounds AS (
    SELECT 
        MIN(DATE_TRUNC('month', order_purchase_timestamp::timestamp)) AS min_month,
        MAX(DATE_TRUNC('month', order_purchase_timestamp::timestamp)) AS max_month
    FROM orders
),
all_months AS (
    SELECT GENERATE_SERIES(min_month, max_month, '1 month'::interval) AS month
    FROM date_bounds
),
monthly_orders AS (
    SELECT 
        DATE_TRUNC('month', order_purchase_timestamp::timestamp) AS month,
        COUNT(*) AS total_orders
    FROM orders
    GROUP BY 1
),
filled_orders AS (
    SELECT 
        a.month,
        COALESCE(m.total_orders, 0) AS total_orders
    FROM all_months a
    LEFT JOIN monthly_orders m ON a.month = m.month
),
lagged_orders AS (
    SELECT 
        month,
        total_orders,
        LAG(total_orders, 1) OVER (ORDER BY month) AS previous_month_orders
    FROM filled_orders
)
SELECT 
    month,
    total_orders,
    COALESCE(previous_month_orders, 0) AS previous_month_orders,
    CASE 
        WHEN previous_month_orders IS NULL THEN NULL 
        WHEN previous_month_orders = 0 AND total_orders = 0 THEN 0.00
        WHEN previous_month_orders = 0 THEN 100.00 
        ELSE ROUND(((total_orders - previous_month_orders)::numeric / previous_month_orders) * 100, 2)
    END AS mom_growth_percent
FROM lagged_orders
ORDER BY month;


-------------------------------------------------------------------
-- Challenge 2: Customer Cohort / Retention Analysis
-------------------------------------------------------------------
WITH customer_first_purchase AS (
    SELECT 
        customer_id,
        MIN(DATE_TRUNC('month', order_purchase_timestamp::timestamp)) AS cohort_month
    FROM orders
    GROUP BY 1
),
cohort_sizes AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) AS total_cohort_customers
    FROM customer_first_purchase
    GROUP BY 1
),
retention_data AS (
    SELECT 
        c.cohort_month,
        DATE_TRUNC('month', o.order_purchase_timestamp::timestamp) AS activity_month,
        COUNT(DISTINCT o.customer_id) AS active_customers
    FROM orders o
    JOIN customer_first_purchase c ON o.customer_id = c.customer_id
    GROUP BY 1, 2
)
SELECT 
    r.cohort_month,
    r.activity_month,
    EXTRACT(YEAR FROM AGE(r.activity_month, r.cohort_month)) * 12 + 
    EXTRACT(MONTH FROM AGE(r.activity_month, r.cohort_month)) AS month_number,
    s.total_cohort_customers,
    r.active_customers,
    ROUND((r.active_customers::numeric / s.total_cohort_customers) * 100, 2) AS retention_rate_percent
FROM retention_data r
JOIN cohort_sizes s ON r.cohort_month = s.cohort_month
ORDER BY r.cohort_month, month_number;


-------------------------------------------------------------------
-- Challenge 3: Running Total (Cumulative Orders)
-------------------------------------------------------------------
WITH monthly_orders AS (
    SELECT 
        DATE_TRUNC('month', order_purchase_timestamp::timestamp) AS month,
        COUNT(*) AS total_orders
    FROM orders
    GROUP BY 1
)
SELECT 
    month,
    total_orders,
    SUM(total_orders) OVER (
        ORDER BY month 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_orders
FROM monthly_orders
ORDER BY month;
