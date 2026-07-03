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

# Pandas program to apply custom functions to columns

import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Salary": [50000, 60000, 70000]
})

# Custom function to categorize salary
def categorize(salary):
    if salary >= 65000:
        return "High"
    elif salary >= 55000:
        return "Medium"
    return "Low"

# Apply function
df["Salary_Tier"] = df["Salary"].apply(categorize)
print(df)
