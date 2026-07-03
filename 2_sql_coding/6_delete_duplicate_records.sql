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

-- SQL Query to delete duplicate records keeping only the unique one (smallest ID)
-- Table Schema: Users(id, email, username)

-- Method 1: Standard DELETE with Subquery (MySQL/Standard SQL)
DELETE FROM Users
WHERE id NOT IN (
    SELECT min_id FROM (
        SELECT MIN(id) AS min_id
        FROM Users
        GROUP BY email
    ) AS temp
);

-- Method 2: Using ROW_NUMBER() in a CTE (SQL Server/PostgreSQL/Oracle)
WITH CTE AS (
    SELECT id,
           ROW_NUMBER() OVER (PARTITION BY email ORDER BY id ASC) as row_num
    FROM Users
)
DELETE FROM Users
WHERE id IN (
    SELECT id FROM CTE WHERE row_num > 1
);
