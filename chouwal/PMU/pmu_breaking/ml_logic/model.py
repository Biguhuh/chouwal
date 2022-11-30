import time
from typing import Tuple
import numpy as np
from pmu_breaking.ml_logic.data import clean_data
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import pandas as pd
import pickle

end = time.perf_counter()

def refining_target():
    db = clean_data()
    mask = db['cl'].str.isnumeric()
    db[mask == False] = 999
    db['cl'] = pd.to_numeric(db['cl'] , errors='coerce') # on convertit toutes les valeurs en valeur int

    # Tous les placés (podiums) prennent la valeur 1
    mask1 = db['cl'] < 4
    db[mask1] = 1

    # Tous les hors podium prennent la valeur 0
    mask2 = db['cl'] > 1
    db[mask2] = 0

    return db

def define_features_target():
    db = refining_target()
    X = db.drop(columns = ['cl'])
    y = db.cl
    features = X.columns
    print("\nFeatures and target defined 🫡")
    # print(f'\n Features :\n {X}')
    # print(f'\n Target :\n {y}')

    return X, y, features

def scaling_imputing():
    #print(f'y : \n{y}')
    X, y, features = define_features_target()
    scaler = StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)

    imputer = SimpleImputer()
    imputer.fit(X)
    X = imputer.transform(X)

    X = pd.DataFrame(X, columns=features)
    print("\nTarget scaled and imputed 🫡")
    return X, y

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

    return model, X_proj, y

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

def save_model():
    # Warning ! This will train again your model then save it
    model = train_model()
    filename = 'pmu_breaking_model.pkl'
    pickle.dump(model, open(filename, 'wb'))
    print('Model Saved 🫡')

def predict(X_test):
    pickled_model = pickle.load(open('pmu_breaking_model.pkl', 'rb'))
    pickled_model.predict(X_test)
