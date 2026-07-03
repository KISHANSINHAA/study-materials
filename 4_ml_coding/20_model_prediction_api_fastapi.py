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

# Model Prediction API using FastAPI
# This sets up a serving API endpoint for a trained ML model.

# Note: Requires fastapi and uvicorn. Can run with: uvicorn 20_model_prediction_api_fastapi:app --reload

try:
    from fastapi import FastAPI
    from pydantic import BaseModel
    import uvicorn
    import numpy as np
    
    # 1. Initialize FastAPI app
    app = FastAPI(title="ML Model Prediction Service")
    
    # 2. Define input schema using Pydantic
    class PredictionRequest(BaseModel):
        feature1: float
        feature2: float
        feature3: float
        
    # 3. Dummy predict function (representing actual model.predict)
    def predict_mock(features):
        # Let's say model output is sum of features > 1.5
        score = sum(features)
        return {"prediction": 1 if score > 1.5 else 0, "probability": float(1 / (1 + np.exp(-score)))}
        
    @app.post("/predict")
    def get_prediction(request: PredictionRequest):
        features = [request.feature1, request.feature2, request.feature3]
        prediction_result = predict_mock(features)
        return prediction_result
        
    @app.get("/")
    def root():
        return {"message": "API is online. Submit POST requests to /predict."}
        
    if __name__ == "__main__":
        print("Starting mock FastAPI server log (simulating).")
        # uvicorn.run(app, host="127.0.0.1", port=8000)
except ImportError:
    print("FastAPI or Uvicorn not installed. To run this file, run: pip install fastapi uvicorn")
