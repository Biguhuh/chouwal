import pickle
import pickle
from model_complet.v1_edouard_preprocessing import clean_data
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
import pandas as pd
import pickle
import os
from model_complet.v1_edouard_preprocessing import transphorm_cl_to_y
from model_complet.v1_edouard_preprocessing import transform_all_non_numerical_value


# Once we are happy with the predicted value or score, we save it
def train_save_model_oct_2022(model_date_csv_path):
    """
    Initialize the Neural Network with random weights
    """
   
    preproc_pipe = make_pipeline(SimpleImputer(),StandardScaler(), PCA())
    
    data = pd.read_csv(model_date_csv_path)
    data = clean_data(data)
    data = transphorm_cl_to_y(data)
    data = transform_all_non_numerical_value(data)
    
    X = data.drop(columns = "cl")
    y = data.cl
    X = preproc_pipe.fit_transform(X)
    model = LogisticRegression()
    model.fit(X, y)

    pickle.dump(model, open('model2.pkl', 'wb'))
    return preproc_pipe

def create_model(path = 'CSV_OCT_2022_PATH'):
    model = train_save_model_oct_2022(os.environ.get(path))
    print('model_creer 🫡')
    return model    

# Predicting from saved model
def predict_from_saved_model(X_pred):
    pickled_model = pickle.load(open('model2.pkl', 'rb'))
    preproc_pipe = train_save_model_oct_2022(os.environ.get('CSV_OCT_2022_PATH'))
    X_pred = preproc_pipe.transform(X_pred)
    print('model loaded 🫡')
    y_pred = pickled_model.predict(X_pred)
    y_pred_proba = pickled_model.predict_proba(X_pred)
    
    return y_pred, y_pred_proba












#################\\model utiliser pour prédire les donner du jour en fonction de la veille//##################
#########################################\\voir les ancien commit//###########################################

def created_X_y(df):
    X = df.drop(columns = "cl")
    y = df.cl
    return X, y


def build_fit_pipeline_for_yesterday(X, y = None):
    """
    Initialize the Neural Network with random weights
    """
   
    preproc_pipe = make_pipeline(SimpleImputer(),StandardScaler(), PCA())
    
    X = preproc_pipe.fit_transform(X)
    
    
    return preproc_pipe, X

def make_pred_frompipe(X_train, X_to_pred, y_train):
    """
    Make a prediction using the latest trained model
    """
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    y_pred_proba = model.predict_proba(X_to_pred)
    y_pred = model.predict(X_to_pred)
    
    return y_pred_proba, y_pred
###############################################################################################################
