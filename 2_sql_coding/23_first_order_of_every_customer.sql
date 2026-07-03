-- ====================================================================
-- THEORY & CONCEPT:
-- SQL query demonstrating structured data selection, joins, window processing, and filtering rules.
--
-- COMPLEXITY:
-- Time Complexity: Depends on indices, usually O(N log N) for sort/joins.
-- Space Complexity: Temporary workspace storage.
--
-- INTERVIEW Q&A:
-- Q: What is a clustered index?
-- A: An index that defines the physical storage order of table data. There can only be one clustered index per table.
--
-- Q: What is a CTE?
-- A: A Common Table Expression is a temporary named result set that can be referenced within a SELECT, INSERT, UPDATE, or DELETE statement.
-- ====================================================================

-- SQL Query to find the first order placed by every customer
-- Table Schema: Orders(id, customer_id, order_date, total_price)

WITH RankedOrders AS (
    SELECT customer_id,
           id AS order_id,
           order_date,
           total_price,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date ASC, id ASC) AS rnk
    FROM Orders
)
SELECT customer_id, order_id, order_date, total_price
FROM RankedOrders
WHERE rnk = 1;
