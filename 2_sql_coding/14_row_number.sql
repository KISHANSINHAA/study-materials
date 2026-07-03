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

-- SQL Query to assign a unique sequence number to each employee using ROW_NUMBER()
-- ROW_NUMBER() assigns a unique number to each row regardless of duplicates.
-- Table Schema: Employee(id, name, salary)

SELECT name,
       salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num
FROM Employee;
