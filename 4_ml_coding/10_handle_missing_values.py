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

# ML Code for Handling Missing Values in a Pipeline

import numpy as np
from sklearn.impute import SimpleImputer

# Dataset with NaN values
X = np.array([[1, 2],
              [np.nan, 3],
              [7, np.nan],
              [10, 12]])

# Impute missing values with column means
imputer = SimpleImputer(strategy="mean")
X_imputed = imputer.fit_transform(X)

print("Original Array with NaNs:\n", X)
print("Imputed Array:\n", X_imputed)
