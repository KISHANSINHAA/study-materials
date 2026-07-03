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

# Pandas program to fill missing values

import pandas as pd
import numpy as np

data = {
    "name": ["Alice", "Bob", "Charlie", "David"],
    "age": [25, np.nan, 35, np.nan],
    "salary": [50000, 60000, np.nan, 80000]
}
df = pd.DataFrame(data)
print("Original:\n", df)

# Fill 'age' with median age, 'salary' with 0
median_age = df["age"].median()
df_filled = df.fillna({"age": median_age, "salary": 0})
print("\nFilled missing values:\n", df_filled)
