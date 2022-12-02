import time
from typing import Tuple
import numpy as np
from pmu_breaking.ml_logic.Model1.v1_edouard_preprocessing import scaling_imputing
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import pandas as pd
import pickle

end = time.perf_counter()

def initialize_model():
    """
    Initialize the Neural Network with random weights
    """
    model = LogisticRegression()
    print("\nModel initialized 🫡")

    return model

def train_model():
    """
    Fit model and return the tuple fitted_model
    """
    X_proj, y = scaling_imputing()
    model = initialize_model()
    model.fit(X_proj, y)
    print(f"\nModel trained ({len(X_proj)} rows) 🫡")
    print("\n Model fit 🫡")

    return model, X_proj, y

# Evaluate basic logistic regression model
def evaluate_model():
    """
    Evaluate trained model performance on dataset
    """
    model, X_proj, y = train_model()
    if model is None:
        print(f"\n❌ no model to evaluate")
        return None
    score = model.score(X_proj, y)
    print(f"\nModel evaluated with score of {score} 🫡")

    return score

# Test predicting first 3 horses (without saved model)
def test_pred(X_pred: pd.DataFrame = None) -> np.ndarray:
    """
    Make a prediction using the latest trained model
    """
    from pmu_breaking.ml_logic.registry import load_model

    if X_pred is None:
        print('No X_pred')

    model = load_model()
    y_pred = model.predict(X_pred)

    print(f"\n✅ Prediction : {y_pred}, with shape {y_pred.shape}")
    return y_pred

# Once we are happy with the predicted value or score, we save it
def save_model():
    # Warning ! This will train again your model then save it
    model = train_model()
    filename = 'pmu_breaking_model.pkl'
    pickle.dump(model, open(filename, 'wb'))
    print('Model Saved 🫡')

# Predicting from saved model
def predict_from_saved_model(X_test):
    pickled_model = pickle.load(open('pmu_breaking_model.pkl', 'rb'))
    pickled_model.predict(X_test)
