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

# Pandas program to remove duplicates

import pandas as pd

data = {
    "id": [1, 2, 2, 3, 1],
    "name": ["Alice", "Bob", "Bob", "Charlie", "Alice"]
}
df = pd.DataFrame(data)
print("Original:\n", df)

# Drop duplicate rows keeping the first occurrence
df_unique = df.drop_duplicates()
print("\nAfter Removing Duplicates:\n", df_unique)
