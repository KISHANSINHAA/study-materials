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

# ML Code for Random Search CV
# More efficient than Grid Search CV for large hyperparameter search spaces.

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV

X = np.random.rand(100, 5)
y = np.random.choice([0, 1], size=100)

model = RandomForestClassifier(random_state=42)

# Distribution parameters
param_distributions = {
    "n_estimators": range(10, 200, 10),
    "max_depth": [3, 5, 7, 10, None],
}

# Search 10 random combinations
random_search = RandomizedSearchCV(
    estimator=model, param_distributions=param_distributions, n_iter=10, cv=3, random_state=42
)
random_search.fit(X, y)

print("Best Parameters:", random_search.best_params_)
print(f"Best CV Score: {random_search.best_score_:.4f}")
