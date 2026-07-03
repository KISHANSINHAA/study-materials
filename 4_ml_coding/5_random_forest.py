# ====================================================================
# THEORY & CONCEPT:
# Random Forest is a bagging ensemble method. It trains multiple decision trees on random subsets of the data (bootstrap samples) and features. It aggregates their predictions (voting/average), reducing overall model variance.
#
# COMPLEXITY:
# Time Complexity: O(M * N * D log N) to train M trees of depth log N.
# Space Complexity: O(M * depth) to store tree nodes.
#
# INTERVIEW Q&A:
# Q: Why does Random Forest reduce overfitting compared to a single Decision Tree?
# A: By training diverse trees on different bootstrap samples and averaging them, individual tree errors cancel out, reducing variance without increasing bias.
#
# Q: What is Out-Of-Bag (OOB) error?
# A: The average error computed on each training sample using only the trees that did not contain that sample in their bootstrap split. It acts as an internal validation score.
# ====================================================================

# ML Code for Random Forest Classifier
# Ensemble learning method using multiple decision trees.

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

X = np.random.rand(100, 4)
y = np.random.choice([0, 1], size=100)

# n_estimators is the number of decision trees in forest
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X, y)

preds = model.predict(X)
print("Random Forest Training Accuracy:", accuracy_score(y, preds))
