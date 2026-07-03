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

-- SQL Query/Function to find the N-th highest salary
-- Table Schema: Employee(id INT, salary INT)

-- Using DENSE_RANK() in a CTE (Common Table Expression)
-- This approach elegantly handles duplicate salaries.
WITH RankedSalaries AS (
    SELECT salary,
           DENSE_RANK() OVER (ORDER BY salary DESC) as rank_num
    FROM Employee
)
SELECT DISTINCT salary AS NthHighestSalary
FROM RankedSalaries
WHERE rank_num = @N; -- Replace @N with desired rank (e.g. 3, 4, etc.)
