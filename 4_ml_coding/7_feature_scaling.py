# ====================================================================
# THEORY & CONCEPT:
# Machine Learning pipeline concept. Focuses on data preprocessing, model selection, evaluation metrics, and hyperparameter optimization.
#
# COMPLEXITY:
# Time Complexity: Training depends heavily on parameters; evaluation is fast O(D).
# Space Complexity: Model representation parameters in RAM.
#
# INTERVIEW Q&A:
# Q: What is overfitting?
# A: When a model learns details and noise in the training data to the extent that it negatively impacts performance on new data.
#
# Q: What is Cross Validation?
# A: A validation technique where the dataset is partitioned into folds, training the model on some folds and validating on others recursively to evaluate performance stability.
# ====================================================================

# ML Code for Feature Scaling
# Standardizes and normalizes features.

import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Original features with different scales
X = np.array([[1.0, 1000.0],
              [2.0, 2000.0],
              [3.0, 1500.0],
              [4.0, 3000.0]])

# 1. StandardScaler (Zero Mean, Unit Variance)
scaler_std = StandardScaler()
X_std = scaler_std.fit_transform(X)

# 2. MinMaxScaler (Scales to [0, 1] range)
scaler_minmax = MinMaxScaler()
X_minmax = scaler_minmax.fit_transform(X)

print("Original Data:\n", X)
print("Standard Scaled Data:\n", X_std)
print("MinMax Scaled Data:\n", X_minmax)
