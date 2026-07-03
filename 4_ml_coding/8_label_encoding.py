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

# ML Code for Label Encoding
# Encodes ordinal categorical text to integer labels (0 to n-classes-1).

from sklearn.preprocessing import LabelEncoder

categories = ["Low", "High", "Medium", "Low", "High"]

encoder = LabelEncoder()
encoded_values = encoder.fit_transform(categories)

print("Original Categories:", categories)
print("Encoded Categories: ", encoded_values)
print("Mapping Classes:    ", list(encoder.classes_))
