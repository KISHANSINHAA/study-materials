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

# ML Code for K-Means Clustering

import numpy as np
from sklearn.cluster import KMeans

# Generate mock 2D data
X = np.random.rand(50, 2)

# Perform clustering with 3 clusters
kmeans = KMeans(n_clusters=3, random_state=42, n_init="auto")
kmeans.fit(X)

# Get predictions and centroids
labels = kmeans.labels_
centroids = kmeans.cluster_centers_

print("Cluster Labels for first 10 items:\n", labels[:10])
print("Cluster Centroids:\n", centroids)
