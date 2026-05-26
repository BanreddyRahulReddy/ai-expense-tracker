"""
classifier.py

PURPOSE: Load the saved model.pkl and expose a simple predict() function.
Flask routes call predict("lunch at cafe") and get back "Food".

You DON'T need to re-train every time the app runs — just load once.
"""

import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print("Classifier model loaded successfully.")
except FileNotFoundError:
    model = None
    print("model.pkl not found. Run: python3 ml/train_classifier.py")


def predict_category(description: str) -> dict:
    if model is None:
        return {"category": "other", "confidence": 0}

    description = description.strip().lower()
    category = model.predict([description])[0]

    # LinearSVC doesn't have predict_proba, so use decision function instead
    decision = model.decision_function([description])[0]
    # Convert to a 0-100 confidence score
    import numpy as np
    scores = np.array(decision)
    best_score = float(np.max(scores))
    confidence = round(min(99.9, max(50.0, 50 + best_score * 10)), 1)

    return {
        "category": category,
        "confidence": confidence
    }