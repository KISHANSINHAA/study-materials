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

# ML Code for Decision Tree Classifier

import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

X = np.random.rand(100, 4)
y = np.random.choice([0, 1], size=100)

# max_depth controls tree growth to prevent overfitting
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X, y)

preds = model.predict(X)
print("Decision Tree Training Accuracy:", accuracy_score(y, preds))
