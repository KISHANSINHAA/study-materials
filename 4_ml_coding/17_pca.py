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

# ML Code for Principal Component Analysis (PCA)
# Reduces features dimension while maximizing variance.

import numpy as np
from sklearn.decomposition import PCA

# Data with 4 features (some highly correlated)
X = np.random.rand(10, 4)

# Keep top 2 principal components
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

print("Original Shape:", X.shape)
print("Reduced Shape: ", X_reduced.shape)
print("Explained Variance Ratio:", pca.explained_variance_ratio_)
