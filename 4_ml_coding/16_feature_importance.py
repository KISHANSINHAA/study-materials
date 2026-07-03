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

# ML Code for Feature Importance
# Identifies which features have the strongest relationship with the target.

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Setup data with named features
X_data = np.random.rand(100, 4)
features = ["age", "income", "credit_score", "savings"]
X = pd.DataFrame(X_data, columns=features)
y = np.random.choice([0, 1], size=100)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Retrieve feature importances
importances = model.feature_importances_

# Display sorted importances
feat_importances = pd.Series(importances, index=X.columns).sort_values(ascending=False)
print("Feature Importances:\n", feat_importances)
