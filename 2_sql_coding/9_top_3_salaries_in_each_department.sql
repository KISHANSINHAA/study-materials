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

-- SQL Query to find the top 3 highest salaries in each department
-- Table Schema:
-- Employee(id, name, salary, departmentId)
-- Department(id, name)

WITH RankedSalaries AS (
    SELECT d.name AS Department,
           e.name AS Employee,
           e.salary AS Salary,
           DENSE_RANK() OVER (PARTITION BY e.departmentId ORDER BY e.salary DESC) as rnk
    FROM Employee e
    JOIN Department d ON e.departmentId = d.id
)
SELECT Department, Employee, Salary
FROM RankedSalaries
WHERE rnk <= 3;
