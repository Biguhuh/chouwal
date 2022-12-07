from model_complet.get_daily_db import get_daily_db
from model_complet.v1_edouard_preprocessing import clean_data
from model_complet.model import created_X_y
from model_complet.v1_edouard_preprocessing import transphorm_cl_to_y
from model_complet.affichage import affichage
from model_complet.model import predict_from_saved_model
from model_complet.model import create_model 
from model_complet.v1_edouard_preprocessing import transform_all_non_numerical_value
import os


if __name__ == '__main__':
    
    ######get data######
    df_today, df_yesterday = get_daily_db() 
    print('dataframes created 🫡')
    
    #######preprocessing#######
    data_to_predict = clean_data(df_today)
    print('columns has been droped🫡')
    data_to_predict = transphorm_cl_to_y(data_to_predict)
    print("\ny has been refined 🫡")
    data_to_predict = transform_all_non_numerical_value(data_to_predict)
    
    
    #########model########
    X_to_pred, y_to_pred = created_X_y(data_to_predict)
    print(X_to_pred.shape)
    if not os.path.exists('model2 .pkl'):
        create_model()
        
    y_pred, y_pred_proba = predict_from_saved_model(X_to_pred)
    
    print(y_pred)
    print("\ny_pred done🫡")
    
    #######affichage#######
    df = affichage(df_today, y_pred, y_pred_proba)
    print(df)
    

