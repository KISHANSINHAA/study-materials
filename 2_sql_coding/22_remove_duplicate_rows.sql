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

-- SQL Query outlining how to delete duplicates on all columns
-- Table Schema: Product(id, name, price, category)

-- Uses CTE to rank rows on duplicate keys and deletes duplicates.
WITH CTE AS (
    SELECT id,
           ROW_NUMBER() OVER (PARTITION BY name, price, category ORDER BY id) as row_num
    FROM Product
)
DELETE FROM Product
WHERE id IN (
    SELECT id FROM CTE WHERE row_num > 1
);
