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

# Pandas Pivot Table

import pandas as pd

data = {
    "city": ["NY", "NY", "SF", "SF", "NY"],
    "year": [2021, 2022, 2021, 2022, 2022],
    "sales": [100, 150, 200, 250, 300]
}
df = pd.DataFrame(data)

# Create Pivot Table
pivot = df.pivot_table(values="sales", index="city", columns="year", aggfunc="sum")
print("Sales Pivot Table:\n", pivot)
