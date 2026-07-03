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

# Pandas Date-Time Operations
# Parsing, formatting, and extracting parts from dates.

import pandas as pd

dates = ["2026-01-01", "2026-06-15", "2026-12-25"]
df = pd.DataFrame({"raw_dates": dates})

# Convert string columns to Datetime
df["parsed_date"] = pd.to_datetime(df["raw_dates"])

# Extract components
df["year"] = df["parsed_date"].dt.year
df["month"] = df["parsed_date"].dt.month
df["day_name"] = df["parsed_date"].dt.day_name()

print(df)
