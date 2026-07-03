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

# ML Code to Save and Load Model using joblib

import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib

X = np.random.rand(10, 2)
y = np.random.choice([0, 1], size=10)

model = LogisticRegression()
model.fit(X, y)

# 1. Save the model to a file
model_filename = "saved_logistic_model.pkl"
joblib.dump(model, model_filename)
print(f"Model saved to: {model_filename}")

# 2. Load the model from file
loaded_model = joblib.load(model_filename)
print("Model successfully reloaded. Coefficients:", loaded_model.coef_)

# Cleanup file
import os
if os.path.exists(model_filename):
    os.remove(model_filename)
