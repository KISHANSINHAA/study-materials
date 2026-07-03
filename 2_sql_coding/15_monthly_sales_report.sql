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

-- SQL Query to generate a monthly sales report with total sales and count of transactions
-- Table Schema: Sales(id, sale_date, amount)

SELECT DATE_FORMAT(sale_date, '%Y-%m') AS sale_month,
       COUNT(id) AS total_transactions,
       SUM(amount) AS total_sales
FROM Sales
GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
ORDER BY sale_month DESC;
