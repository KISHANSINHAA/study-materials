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

# Pandas value_counts to count occurrences of unique values

import pandas as pd

df = pd.DataFrame({
    "feedback": ["Good", "Bad", "Good", "Excellent", "Good", "Bad"]
})

# Count frequency of each unique feedback category
counts = df["feedback"].value_counts()
print("Value Counts:\n", counts)
