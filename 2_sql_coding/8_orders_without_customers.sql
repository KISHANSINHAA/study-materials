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

-- SQL Query to find orders that reference non-existent customers
-- Table Schema:
-- Customers(id, name)
-- Orders(id, customerId)

-- Useful for identifying database integrity / orphaned records issues.
SELECT o.id AS OrderID, o.customerId AS CustomerID
FROM Orders o
LEFT JOIN Customers c ON o.customerId = c.id
WHERE c.id IS NULL;
