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

-- SQL Query to rank employees based on their salary using RANK()
-- RANK() skips numbers if there are duplicate values. (e.g. 1, 2, 2, 4)
-- Table Schema: Employee(id, name, salary)

SELECT name,
       salary,
       RANK() OVER (ORDER BY salary DESC) AS salary_rank
FROM Employee;
