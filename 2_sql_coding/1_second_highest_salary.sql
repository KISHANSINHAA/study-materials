-- ====================================================================
-- THEORY & CONCEPT:
-- To find the second highest value, we filter out the absolute maximum salary and select the maximum of the remaining salaries. Alternatively, we rank unique salaries in descending order using DENSE_RANK() and select the salary ranked 2nd.
--
-- COMPLEXITY:
-- Time Complexity: O(N) scan of the table.
-- Space Complexity: O(1) auxiliary space (or O(N) for window rankings).
--
-- INTERVIEW Q&A:
-- Q: How do you ensure the query returns NULL if there is no second highest salary?
-- A: By wrapping the select statement inside a scalar subquery. If the subquery finds no row, SQL returns NULL.
--
-- Q: Why use DENSE_RANK() instead of RANK()?
-- A: DENSE_RANK() assigns consecutive ranks for identical values (e.g. 1, 2, 2, 3), whereas RANK() leaves gaps (e.g. 1, 2, 2, 4), which would break the logic for finding the 3rd highest salary if there are ties.
-- ====================================================================

-- SQL Query to find the second highest salary from the Employee table
-- Table Schema: Employee(id INT, salary INT)

-- Method 1: Using Subquery with MAX()
-- This is highly compatible and works in almost all SQL dialects.
-- It returns NULL if no second highest salary exists.
SELECT MAX(salary) AS SecondHighestSalary
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);

-- Method 2: Using DENSE_RANK() window function
-- Recommended if there are multiple employees with the same salaries.
WITH RankedSalaries AS (
    SELECT salary,
           DENSE_RANK() OVER (ORDER BY salary DESC) as rank_val
    FROM Employee
)
SELECT MAX(salary) AS SecondHighestSalary
FROM RankedSalaries
WHERE rank_val = 2;
