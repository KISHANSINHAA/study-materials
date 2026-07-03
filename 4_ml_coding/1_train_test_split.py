# ====================================================================
# THEORY & CONCEPT:
# Splitting a dataset evaluates model generalization. Stratification ensures that the training and testing sets maintain the same class label distributions as the original dataset, which is critical for imbalanced classes.
#
# COMPLEXITY:
# Time Complexity: O(N) to copy and shuffle dataset.
# Space Complexity: O(N) to store split subsets.
#
# INTERVIEW Q&A:
# Q: Why is stratify=y crucial in classification splits?
# A: Without stratification, a rare class might end up entirely in the training set or test set, preventing fair validation and model training.
#
# Q: What is data leakage?
# A: When information from the test set leaks into the training set (e.g. scaling features on the entire dataset before splitting).
# ====================================================================

# ML Code for Train-Test Split
# Splits dataset into training and testing sets.

import numpy as np
from sklearn.model_selection import train_test_split

# Generate mock data
# X: Features (100 rows, 3 columns), y: Target (100 values)
X = np.random.rand(100, 3)
y = np.random.choice([0, 1], size=100)

# Split with 80% train and 20% test
# stratify=y preserves class ratio in target y
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"Total size: X={X.shape}, y={y.shape}")
print(f"Train size: X_train={X_train.shape}, y_train={y_train.shape}")
print(f"Test size:  X_test={X_test.shape}, y_test={y_test.shape}")
