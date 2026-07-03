-- ====================================================================
-- THEORY & CONCEPT:
-- We want to compare individual salaries to the group average. Because aggregate functions like AVG() cannot be evaluated in the WHERE clause directly, we must calculate the average in a subquery.
--
-- COMPLEXITY:
-- Time Complexity: O(N) to calculate average and scan table.
-- Space Complexity: O(1) auxiliary space.
--
-- INTERVIEW Q&A:
-- Q: Why can't we write: WHERE salary > AVG(salary)?
-- A: Aggregate functions operate on groups of rows, whereas the WHERE clause filters individual rows before grouping occurs. A subquery solves this.
--
-- Q: What is a correlated subquery?
-- A: A subquery that references columns from the outer query, executing once for each row in the outer table. The average query here is uncorrelated (runs only once).
-- ====================================================================

-- SQL Query to find employees who earn more than the average salary of the entire company
-- Table Schema: Employee(id, name, salary)

SELECT name AS Employee, salary AS Salary
FROM Employee
WHERE salary > (SELECT AVG(salary) FROM Employee);
