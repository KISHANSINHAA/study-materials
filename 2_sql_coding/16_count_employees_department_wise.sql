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

-- SQL Query to get the count of employees in each department
-- Table Schema: Employee(id, name, departmentId)
-- Department(id, name)

SELECT d.name AS Department,
       COUNT(e.id) AS EmployeeCount
FROM Department d
LEFT JOIN Employee e ON d.id = e.departmentId
GROUP BY d.name
ORDER BY EmployeeCount DESC;
