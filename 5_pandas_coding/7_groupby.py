# ====================================================================
# THEORY & CONCEPT:
# Pandas data wrangling. Manipulates structures in memory using vectorised operations on Series and DataFrames.
#
# COMPLEXITY:
# Time Complexity: O(N) vector operations.
# Space Complexity: O(N) RAM allocation.
#
# INTERVIEW Q&A:
# Q: What is vectorization in Pandas?
# A: Performing operations on entire arrays instead of looping through individual elements, leveraging fast underlying C libraries.
#
# Q: What is the difference between loc and iloc?
# A: loc accesses rows/columns by labels/names. iloc accesses them by integer index positions.
# ====================================================================

# Pandas GroupBy and aggregation

import pandas as pd

data = {
    "dept": ["HR", "IT", "IT", "HR", "Sales"],
    "salary": [50000, 80000, 90000, 55000, 65000],
    "bonus": [5000, 8000, 7000, 4000, 6000]
}
df = pd.DataFrame(data)

# Group by dept and calculate mean salary & sum bonus
grouped = df.groupby("dept").agg({
    "salary": "mean",
    "bonus": "sum"
}).rename(columns={"salary": "avg_salary", "bonus": "total_bonus"})

print("Grouped Results:\n", grouped)
