from sklearn import svm
from sklearn import datasets
import pickle
from sklearn import svm
from sklearn import datasets
import pickle
import time
from typing import Tuple
import numpy as np
from model_complet.v1_edouard_preprocessing import clean_data
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
import pandas as pd
import csv
import pickle

end = time.perf_counter()

def created_X_y(df):
    X = df.drop(columns = "cl")
    y = df.cl
    return X, y

def build_fit_pipeline(X, y = None):
    """
    Initialize the Neural Network with random weights
    """
   
    preproc_pipe = make_pipeline(SimpleImputer(),StandardScaler(), PCA())
    
    X = preproc_pipe.fit_transform(X)
    
    return preproc_pipe, X
'''
def train_model():
    """
    Fit model and return the tuple fitted_model
    """
    X_proj, y = scaling_imputing()
    model = initialize_model()
    model.fit(X_proj, y)
    print(f"\nModel trained ({len(X_proj)} rows) 🫡")
    print("\nModel fit 🫡")

    return model, X_proj, y
'''

# Evaluate basic logistic regression model
def evaluate_model(model, X, y):
    """
    Evaluate trained model performance on dataset
    """
    score = model.score(X, y)
    print(f"\nModel evaluated with score of {score} 🫡")

    return None

# Test predicting first 3 horses (without saved model)
def make_pred(X_train, X_to_pred, y_train):
    """
    Make a prediction using the latest trained model
    """
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict_proba(X_to_pred)

    return y_pred

# Once we are happy with the predicted value or score, we save it
def train_save_model():
    model, X_proj, y = train_model()
    # Warning ! This will train again your model then save it
    model.fit(X_proj, y)

    s = pickle.dumps(model)
    clf2 = pickle.loads(s)
    clf2.predict(X_proj[0:1])
    model = train_model()

def predict_save_model(to_predict):
    X_today_nb_edouard = pd.read_csv("pmu_results.csv")

    my_pipeline = pickle.load(open("/pipeline.pkl","rb"))
    predicted_class = my_pipeline.predict(new_data.iloc[0:2])
    print(f'Predicted value : {predict_save_model}')
    '''
    with open("'pmu_model_results.csv'",'rb') as f_input:
        model = pickle.loads(f_input) # maybe handled with a singleton to reduce loading for multiple predictions
        filename = 'pmu_breaking_model.pkl'
        pickle.dump(model, open(filename, 'wb'))
    '''


def load_model():
    clf = svm.SVC()
    X, y= datasets.load_iris(return_X_y=True)
    clf.fit(X, y)
    s = pickle.dumps(clf)
    clf2 = pickle.loads(s)
    clf2.predict(X[0:1])

# Predicting from saved model
def predict_from_saved_model(X_test):
    pickled_model = pickle.load(open('pmu_breaking_model.pkl', 'rb'))
    pickled_model.predict(X_test)
