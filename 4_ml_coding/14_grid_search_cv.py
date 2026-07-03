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

# ML Code for Grid Search CV (Hyperparameter Tuning)

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

X = np.random.rand(100, 5)
y = np.random.choice([0, 1], size=100)

model = RandomForestClassifier(random_state=42)

# Hyperparameter grid to explore
param_grid = {
    "n_estimators": [10, 50, 100],
    "max_depth": [3, 5, None],
    "criterion": ["gini", "entropy"]
}

# Grid Search with 3-fold cross validation
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring="accuracy")
grid_search.fit(X, y)

print("Best Parameters:", grid_search.best_params_)
print(f"Best CV Score: {grid_search.best_score_:.4f}")
