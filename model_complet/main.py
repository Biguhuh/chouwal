from model_complet.get_daily_db import get_daily_db
from model_complet.v1_edouard_preprocessing import clean_data
from model_complet.model import make_pred #evaluate_model
#from model_complet.model import predict_from_saved_model
from model_complet.model import build_fit_pipeline
from model_complet.model import created_X_y


if __name__ == '__main__':
    
    ######get data######
    df_today, df_yesterday = get_daily_db() 
    print('dataframes created 🫡')
    
    #######preprocessing#######
    data_train = clean_data(df_yesterday) 
    data_to_predict = clean_data(df_today)
    print('columns has been droped🫡')
    print("\ny has been refined 🫡")
    
    #########model########
    X_train, y_train = created_X_y(data_train)
    X_to_pred, y_to_pred = created_X_y(data_to_predict)
    pipe, feature_name, X_train_PCA = build_fit_pipeline(X_train, y_train)
    print("\nPipeline initialized 🫡")
    print(f"\nModel trained ({len(X_train)} rows) 🫡")
    print("\nPipeline fit 🫡")
    pipe, feature_name, X_proj = build_fit_pipeline(X_to_pred)
    
    #evaluate_model(pipe, X, y) # bonus , vraiment pas obligatoire + manque un train_test_split(sinon leackage)
    y_pred = make_pred(X_train, X_proj, y_train)
    print(f"✅ Prediction:\n{y_pred}, with shape {y_pred.shape}")

