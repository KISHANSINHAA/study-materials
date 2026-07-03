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

-- SQL Query to find the third highest salary in the Employee table
-- Table Schema: Employee(id, salary)

WITH RankedSalaries AS (
    SELECT salary,
           DENSE_RANK() OVER (ORDER BY salary DESC) as rank_val
    FROM Employee
)
SELECT DISTINCT salary AS ThirdHighestSalary
FROM RankedSalaries
WHERE rank_val = 3;
