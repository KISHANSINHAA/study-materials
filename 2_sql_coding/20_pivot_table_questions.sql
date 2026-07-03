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

-- SQL Query demonstrating pivoting (converting row values to columns)
-- Task: Get total sales for years 2020, 2021, and 2022 for each product.
-- Table Schema: ProductSales(product_name, sale_year, sale_amount)

SELECT product_name,
       SUM(CASE WHEN sale_year = 2020 THEN sale_amount ELSE 0 END) AS Sales_2020,
       SUM(CASE WHEN sale_year = 2021 THEN sale_amount ELSE 0 END) AS Sales_2021,
       SUM(CASE WHEN sale_year = 2022 THEN sale_amount ELSE 0 END) AS Sales_2022
FROM ProductSales
GROUP BY product_name;
