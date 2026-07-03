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

# ML Code for Cross Validation

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

X = np.random.rand(200, 5)
y = np.random.choice([0, 1], size=200)

model = RandomForestClassifier(n_estimators=10, random_state=42)

# Compute 5-fold cross validation score
scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")

print("CV Scores (5 folds):", scores)
print(f"Mean Accuracy: {scores.mean():.4f} +/- {scores.std():.4f}")
