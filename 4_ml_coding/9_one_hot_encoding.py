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

# ML Code for One-Hot Encoding
# Converts categorical values into binary columns.

import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Method 1: Using Pandas get_dummies (Fastest for prototyping)
data = {"color": ["red", "blue", "green", "blue"]}
df = pd.DataFrame(data)
df_encoded_pandas = pd.get_dummies(df, columns=["color"], dtype=int)
print("Pandas get_dummies Output:\n", df_encoded_pandas)

# Method 2: Using Sklearn OneHotEncoder (Best for production pipelines)
encoder = OneHotEncoder(sparse_output=False)
encoded_array = encoder.fit_transform(df[["color"]])
print("\nSklearn OneHotEncoder Array:\n", encoded_array)
print("Feature Names:", encoder.get_feature_names_out())
