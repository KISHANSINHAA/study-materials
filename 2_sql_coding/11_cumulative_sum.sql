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

-- SQL Query to calculate cumulative sum of sales by month
-- Table Schema: MonthlySales(year_val, month_val, sales_amount)

SELECT year_val,
       month_val,
       sales_amount,
       SUM(sales_amount) OVER (PARTITION BY year_val ORDER BY month_val ASC) AS cumulative_sales_yearwise
FROM MonthlySales;
