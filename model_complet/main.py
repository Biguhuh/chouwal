from model_complet.get_daily_db import get_daily_db
from model_complet.v1_edouard_preprocessing import clean_data
from model_complet.model import make_pred #evaluate_model
#from model_complet.model import predict_from_saved_model
from model_complet.model import build_fit_pipeline


if __name__ == '__main__':
    
    ######get data######
    df_today, df_yesterday = get_daily_db() 
    
    #######preprocessing#######
    db = clean_data(df_today) 
    
    #########model########
    pipe, feature_name, X, y = build_fit_pipeline(db)
    #evaluate_model(pipe, X, y) # bonus , vraiment pas obligatoire + manque un train_test_split(sinon leackage)
    y_pred = make_pred()

    print(f"y_pred: {y_pred}")
