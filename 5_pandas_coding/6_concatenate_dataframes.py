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

# Pandas program to concatenate DataFrames
# Stacks DataFrames vertically (axis=0) or horizontally (axis=1).

import pandas as pd

df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df2 = pd.DataFrame({"A": [5, 6], "B": [7, 8]})

# Vertical concatenation (row-wise)
vertical = pd.concat([df1, df2], axis=0, ignore_index=True)
print("Vertical Concatenation:\n", vertical)

# Horizontal concatenation (column-wise)
horizontal = pd.concat([df1, df2], axis=1)
print("\nHorizontal Concatenation:\n", horizontal)
