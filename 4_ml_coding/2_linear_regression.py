# ====================================================================
# THEORY & CONCEPT:
# Linear Regression models a continuous target variable y by finding weights w that minimize the Mean Squared Error (MSE) using Ordinary Least Squares: RSS = sum(y_actual - y_pred)^2.
#
# COMPLEXITY:
# Time Complexity: O(N * D^2 + D^3) where N is samples, D is features (analytical solve).
# Space Complexity: O(D) to store coefficients.
#
# INTERVIEW Q&A:
# Q: What are the assumptions of Linear Regression?
# A: Linearity, independence of errors, homoscedasticity (constant variance of residuals), and normality of residuals.
#
# Q: What does R-squared measure?
# A: The proportion of variance in the dependent variable that is predictable from the independent variables (scale of 0 to 1).
# ====================================================================

# ML Code for Linear Regression
# Fits line/hyperplane to predict a continuous target variable.

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Mock data: Y = 2*X_1 + 3*X_2 + noise
np.random.seed(42)
X = np.random.rand(100, 2)
y = 2 * X[:, 0] + 3 * X[:, 1] + np.random.normal(0, 0.1, 100)

# Instantiate and fit
model = LinearRegression()
model.fit(X, y)

# Predict and Evaluate
predictions = model.predict(X)
mse = mean_squared_error(y, predictions)
r2 = r2_score(y, predictions)

print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)
print("Mean Squared Error (MSE):", mse)
print("R-squared (R2) score:", r2)
