# ====================================================================
# THEORY & CONCEPT:
# Handling missing data (NaN). Dropping missing values deletes incomplete records, preventing model skewing but reducing sample size. Imputing values (filling) preserves sample size but introduces bias.
#
# COMPLEXITY:
# Time Complexity: O(N) to locate and modify NaN values.
# Space Complexity: O(1) if modified in-place; O(N) if generating a copy.
#
# INTERVIEW Q&A:
# Q: What is the difference between dropna(how='any') and dropna(how='all')?
# A: how='any' drops the row if any column contains NaN. how='all' drops the row only if all columns are NaN.
#
# Q: Why is inplace=True sometimes discouraged?
# A: It doesn't always save memory due to pandas' internal copying mechanisms, and it breaks method chaining pipelines.
# ====================================================================

# Pandas program to drop missing values (NaN)

import pandas as pd
import numpy as np

data = {
    "name": ["Alice", "Bob", np.nan, "David"],
    "age": [25, np.nan, np.nan, 40],
    "salary": [50000, 60000, 70000, 80000]
}
df = pd.DataFrame(data)
print("Original:\n", df)

# 1. Drop rows with any NaN
drop_any = df.dropna()
print("\nDrop rows with ANY NaN:\n", drop_any)

# 2. Drop rows with NaN in specific columns
drop_subset = df.dropna(subset=["name"])
print("\nDrop rows with NaN in 'name':\n", drop_subset)
