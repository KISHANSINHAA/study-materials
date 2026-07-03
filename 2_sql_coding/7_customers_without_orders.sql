-- ====================================================================
-- THEORY & CONCEPT:
-- Finding orphan records in Table A that do not have matching keys in Table B. This is achieved using a LEFT JOIN and checking for NULL in Table B's primary key, or using a NOT IN / NOT EXISTS subquery.
--
-- COMPLEXITY:
-- Time Complexity: O(N log N) for join/lookup operations.
-- Space Complexity: O(N) to execute the join.
--
-- INTERVIEW Q&A:
-- Q: Why is NOT EXISTS preferred over NOT IN?
-- A: If Table B contains any NULL value in the key column, NOT IN will return zero rows. NOT EXISTS is null-safe and optimized by query plan compilers.
--
-- Q: What does a LEFT JOIN return if there is no match?
-- A: It returns the row from the left table with all columns from the right table filled with NULL.
-- ====================================================================

-- SQL Query to find all customers who never ordered anything
-- Table Schema:
-- Customers(id, name)
-- Orders(id, customerId)

-- Method 1: Using LEFT JOIN and filtering NULLs (Often highly performant)
SELECT c.name AS Customers
FROM Customers c
LEFT JOIN Orders o ON c.id = o.customerId
WHERE o.id IS NULL;

-- Method 2: Using NOT IN
SELECT name AS Customers
FROM Customers
WHERE id NOT IN (
    SELECT DISTINCT customerId
    FROM Orders
);
