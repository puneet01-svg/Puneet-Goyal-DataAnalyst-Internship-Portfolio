/* =====================================================================
   TASK 2 : SQL & DATA EXTRACTION
   Database : shop.db  (SQLite)
   Schema   : customers, categories, products, orders, order_items
   =====================================================================
   This file is organized to mirror the task plan exactly:
     PART 1  -> Day 9-11  : SQL Fundamentals
     PART 2  -> Day 12-14 : Advanced SQL
   Every query below was executed and validated against shop.db.
   ===================================================================== */


/* =====================================================================
   PART 1 — DAY 9-11 : SQL FUNDAMENTALS
   ===================================================================== */

-- 1.1  SELECT / WHERE / ORDER BY / LIMIT
-- All completed orders placed in the last quarter of the dataset,
-- highest value first, top 10 only.
SELECT order_id, customer_id, order_date, order_total
FROM orders
WHERE status = 'completed'
  AND order_date >= '2026-01-01'
ORDER BY order_total DESC
LIMIT 10;


-- 1.2  WHERE with multiple conditions + pattern matching
SELECT full_name, city, email
FROM customers
WHERE city IN ('Delhi', 'Mumbai', 'Bengaluru')
  AND full_name LIKE 'A%'
ORDER BY full_name
LIMIT 20;


-- 1.3  INNER JOIN
-- Every order line with product and customer names attached.
SELECT o.order_id, c.full_name, p.product_name, oi.quantity, oi.unit_price
FROM orders o
INNER JOIN customers c   ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON oi.order_id = o.order_id
INNER JOIN products p    ON p.product_id = oi.product_id
ORDER BY o.order_id
LIMIT 20;


-- 1.4  LEFT JOIN
-- All customers, including those who have never placed an order
-- (order columns will be NULL for them).
SELECT c.customer_id, c.full_name, o.order_id, o.order_total
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
ORDER BY c.customer_id
LIMIT 20;


-- 1.5  RIGHT JOIN
-- Every order paired with its product line items, keeping all order_items
-- even in the hypothetical case an order header row were missing.
SELECT oi.order_item_id, oi.order_id, o.order_date, oi.quantity
FROM orders o
RIGHT JOIN order_items oi ON oi.order_id = o.order_id
ORDER BY oi.order_item_id
LIMIT 20;


-- 1.6  FULL (OUTER) JOIN
-- Categories vs products: shows categories with zero products (none here)
-- and products with no category (none here) — a full audit view.
SELECT cat.category_id, cat.category_name, p.product_id, p.product_name
FROM categories cat
FULL JOIN products p ON p.category_id = cat.category_id
ORDER BY cat.category_id;


-- 1.7  GROUP BY + aggregate functions (COUNT, SUM, AVG, MIN, MAX)
SELECT
    cat.category_name,
    COUNT(DISTINCT p.product_id)      AS product_count,
    SUM(oi.quantity)                  AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
    ROUND(AVG(oi.unit_price), 2)      AS avg_unit_price,
    MIN(oi.unit_price)                AS cheapest_line,
    MAX(oi.unit_price)                AS priciest_line
FROM categories cat
JOIN products p     ON p.category_id = cat.category_id
JOIN order_items oi ON oi.product_id = p.product_id
GROUP BY cat.category_name
ORDER BY revenue DESC;


-- 1.8  GROUP BY + HAVING
-- Customers who have generated more than 50,000 in completed order value.
SELECT c.customer_id, c.full_name, SUM(o.order_total) AS total_spend
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.full_name
HAVING SUM(o.order_total) > 50000
ORDER BY total_spend DESC;


-- 1.9  Subquery (non-correlated)
-- Products priced above the overall average unit price.
SELECT product_name, unit_price
FROM products
WHERE unit_price > (SELECT AVG(unit_price) FROM products)
ORDER BY unit_price DESC;


-- 1.10 Subquery (correlated)
-- Each customer's most recent order date, via a correlated subquery.
SELECT c.customer_id, c.full_name,
       (SELECT MAX(o.order_date)
        FROM orders o
        WHERE o.customer_id = c.customer_id) AS last_order_date
FROM customers c
ORDER BY last_order_date DESC
LIMIT 15;


-- 1.11 CTE (WITH clause)
-- Revenue per customer, then filter using the CTE like a temp table.
WITH customer_revenue AS (
    SELECT customer_id, SUM(order_total) AS total_revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
)
SELECT c.full_name, cr.total_revenue
FROM customer_revenue cr
JOIN customers c ON c.customer_id = cr.customer_id
WHERE cr.total_revenue > (SELECT AVG(total_revenue) FROM customer_revenue)
ORDER BY cr.total_revenue DESC
LIMIT 15;


-- 1.12 Window functions: ROW_NUMBER, RANK, LAG, LEAD
-- Rank each customer's orders by date and compare to the previous/next order.
SELECT
    o.customer_id,
    o.order_id,
    o.order_date,
    o.order_total,
    ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.order_date) AS order_seq,
    RANK()       OVER (PARTITION BY o.customer_id ORDER BY o.order_total DESC) AS spend_rank,
    LAG(o.order_total)  OVER (PARTITION BY o.customer_id ORDER BY o.order_date) AS prev_order_total,
    LEAD(o.order_total) OVER (PARTITION BY o.customer_id ORDER BY o.order_date) AS next_order_total
FROM orders o
WHERE o.customer_id = 1
ORDER BY o.order_date;



/* =====================================================================
   PART 2 — DAY 12-14 : ADVANCED SQL (business queries)
   ===================================================================== */

-- 2.1  Monthly sales trend
-- Total completed revenue and order count per calendar month.
SELECT
    strftime('%Y-%m', order_date) AS month,
    COUNT(*)                      AS orders_count,
    ROUND(SUM(order_total), 2)    AS monthly_revenue
FROM orders
WHERE status = 'completed'
GROUP BY month
ORDER BY month;


-- 2.2  Top 10 customers by revenue
SELECT c.customer_id, c.full_name, c.city,
       ROUND(SUM(o.order_total), 2) AS total_revenue,
       COUNT(o.order_id)            AS orders_placed
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.full_name, c.city
ORDER BY total_revenue DESC
LIMIT 10;


-- 2.3  Customer retention rate (month-over-month)
-- A customer is "retained" in month M if they also ordered in month M-1.
WITH monthly_customers AS (
    SELECT DISTINCT customer_id,
           strftime('%Y-%m', order_date) AS month
    FROM orders
    WHERE status = 'completed'
),
retention AS (
    SELECT cur.month,
           COUNT(DISTINCT cur.customer_id) AS active_customers,
           COUNT(DISTINCT prev.customer_id) AS retained_customers
    FROM monthly_customers cur
    LEFT JOIN monthly_customers prev
           ON prev.customer_id = cur.customer_id
          AND prev.month = strftime('%Y-%m', date(cur.month || '-01', '-1 month'))
    GROUP BY cur.month
)
SELECT month,
       active_customers,
       retained_customers,
       ROUND(100.0 * retained_customers / active_customers, 1) AS retention_rate_pct
FROM retention
ORDER BY month;


-- 2.4  Product category performance
-- Revenue, units sold, and share of total revenue per category.
WITH category_sales AS (
    SELECT cat.category_name,
           SUM(oi.quantity) AS units_sold,
           SUM(oi.quantity * oi.unit_price) AS revenue
    FROM categories cat
    JOIN products p     ON p.category_id = cat.category_id
    JOIN order_items oi ON oi.product_id = p.product_id
    JOIN orders o       ON o.order_id = oi.order_id
    WHERE o.status = 'completed'
    GROUP BY cat.category_name
)
SELECT category_name,
       units_sold,
       ROUND(revenue, 2) AS revenue,
       ROUND(100.0 * revenue / SUM(revenue) OVER (), 1) AS pct_of_total_revenue
FROM category_sales
ORDER BY revenue DESC;


-- 2.5  Moving average and cumulative sum of daily revenue
-- 7-day moving average of revenue plus a running (cumulative) total.
WITH daily_revenue AS (
    SELECT order_date, SUM(order_total) AS revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY order_date
)
SELECT
    order_date,
    revenue,
    ROUND(AVG(revenue) OVER (
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg_7day,
    ROUND(SUM(revenue) OVER (
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS cumulative_revenue
FROM daily_revenue
ORDER BY order_date
LIMIT 30;


-- 2.6  Views for frequently used queries
-- A view exposing customer lifetime value, ready to query like a table.
DROP VIEW IF EXISTS vw_customer_ltv;
CREATE VIEW vw_customer_ltv AS
SELECT c.customer_id,
       c.full_name,
       c.city,
       COUNT(o.order_id)              AS total_orders,
       ROUND(SUM(o.order_total), 2)   AS lifetime_value,
       MIN(o.order_date)              AS first_order_date,
       MAX(o.order_date)              AS last_order_date
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'completed'
GROUP BY c.customer_id, c.full_name, c.city;

-- Usage example:
SELECT * FROM vw_customer_ltv ORDER BY lifetime_value DESC LIMIT 10;

-- A second view: monthly category revenue, reusable for dashboards.
DROP VIEW IF EXISTS vw_monthly_category_revenue;
CREATE VIEW vw_monthly_category_revenue AS
SELECT
    strftime('%Y-%m', o.order_date) AS month,
    cat.category_name,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p      ON p.product_id = oi.product_id
JOIN categories cat  ON cat.category_id = p.category_id
WHERE o.status = 'completed'
GROUP BY month, cat.category_name;

SELECT * FROM vw_monthly_category_revenue ORDER BY month, revenue DESC LIMIT 20;


-- 2.7  Query optimization: EXPLAIN and indexing
-- Baseline plan before indexing (SQLite will show a full table scan on
-- orders.customer_id when filtering/joining on it without an index).
EXPLAIN QUERY PLAN
SELECT customer_id, COUNT(*) FROM orders WHERE customer_id = 42 GROUP BY customer_id;

-- Add indexes on the foreign key / filter columns most queries above rely on.
CREATE INDEX IF NOT EXISTS idx_orders_customer_id  ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_status_date   ON orders(status, order_date);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product  ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_products_category     ON products(category_id);

-- Re-run EXPLAIN QUERY PLAN after indexing — should now report
-- "SEARCH orders USING INDEX idx_orders_customer_id" instead of a full scan.
EXPLAIN QUERY PLAN
SELECT customer_id, COUNT(*) FROM orders WHERE customer_id = 42 GROUP BY customer_id;

EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE status = 'completed' AND order_date >= '2026-01-01';
