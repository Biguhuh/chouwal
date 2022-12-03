from sklearn import svm
from sklearn import datasets
import pickle
from sklearn import svm
from sklearn import datasets
import pickle
import time
from typing import Tuple
import numpy as np
from pmu_breaking.ml_logic.Model1.v1_edouard_preprocessing import scaling_imputing
from pmu_breaking.ml_logic.Model1.v1_edouard_preprocessing import pca
from pmu_breaking.ml_logic.Model1.v1_edouard_preprocessing import load_model
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import pandas as pd
import csv
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
    X_proj, y = pca()
    X_train, X_test, y_train, y_test = train_test_split(X_proj, y, test_size=0.30)
    model = initialize_model()
    model.fit(X_train, y_train)
    print(f"\nModel trained ({len(X_proj)} rows) 🫡")
    print("\n Model fit 🫡")

    return model, X_test, y_test

'''
def load_model():
    model, X_test, y_test = train_model()
    s = pickle.dumps(model)
    model_loaded = pickle.loads(s)

    print('Model loaded 🫡\n')
    return model_loaded, X_test, y_test
'''

# Test predicting first 3 horses (without saved model)
def today_test_pred():
    """
    Make a prediction using the latest trained model
    """
    # X_today_proj = # a charger
    X_today_proj = pca(X_today)
    model = train_model()[0]

    y_pred_today = model.predict(X_today)

    print(f"\n✅ Prediction : {y_pred_today}, with shape {y_pred_today.shape}")
    return y_pred_today

# Evaluate basic logistic regression model
# /!\ After prediction !!!!
def evaluate_model():
    """
    Evaluate trained model performance on dataset
    """
    model, X_test, y_test = train_model()
    y_test = today_test_pred()

    if model is None:
        print(f"\n❌ no model to evaluate")
        return None
    precision = model.precision_score(y_test, y_pred)
    print(f"\nModel evaluated with precision of {precision} 🫡")

    return y_pred, precision
'''
# Once we are happy with the predicted value or score, we save it
def save_model():
    model, X_proj, y = train_model()
    # Warning ! This will train again your model then save it
    model.fit(X_proj, y)

    s = pickle.dumps(model)
    clf2 = pickle.loads(s)
    clf2.predict(X_proj[0:1])
    model = train_model()
'''
def predict_save_model(to_predict):
    new_data = pd.read_csv("pmu_results.csv")
    new_data
    my_pipeline = pickle.load(open("/pipeline.pkl","rb"))
    predicted_class = my_pipeline.predict(new_data.iloc[0:2])
    print(f'Predicted value : {predict_save_model}')
    '''
    with open("'pmu_model_results.csv'",'rb') as f_input:
        model = pickle.loads(f_input) # maybe handled with a singleton to reduce loading for multiple predictions
        filename = 'pmu_breaking_model.pkl'
        pickle.dump(model, open(filename, 'wb'))
    '''

# Predicting from saved model
def predict_from_saved_model(X_test):
    pickled_model = pickle.load(open('pmu_breaking_model.pkl', 'rb'))
    pickled_model.predict(X_test)
