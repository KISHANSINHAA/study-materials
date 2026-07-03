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

-- SQL Query to find users who logged in for 3 or more consecutive days
-- Table Schema: Logins(user_id, login_date)

WITH RankedLogins AS (
    SELECT DISTINCT user_id,
           login_date,
           -- Subtract RowNumber from date to group consecutive dates together
           login_date - INTERVAL ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) DAY AS date_group
    FROM Logins
)
SELECT user_id,
       MIN(login_date) AS streak_start,
       MAX(login_date) AS streak_end,
       COUNT(*) AS consecutive_days
FROM RankedLogins
GROUP BY user_id, date_group
HAVING COUNT(*) >= 3;
