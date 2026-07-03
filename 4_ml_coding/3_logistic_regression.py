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

# ML Code for Logistic Regression
# Binary classification model outputting class probabilities.

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score

# Mock binary classification data
np.random.seed(42)
X = np.random.randn(100, 2)
# Target depends on sum of inputs
y = (X[:, 0] + X[:, 1] > 0).astype(int)

# Instantiate and fit
model = LogisticRegression()
model.fit(X, y)

# Evaluate
preds = model.predict(X)
probs = model.predict_proba(X)[:, 1] # Probability of class 1

print("Accuracy:", accuracy_score(y, preds))
print("ROC AUC Score:", roc_auc_score(y, probs))
