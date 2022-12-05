from model_complet.get_daily_db import get_daily_db
from model_complet.v1_edouard_preprocessing import to_df, clean_data, refining_target, define_features_target, scaling_imputing
from model_complet.model import make_pred, initialize_model, train_model, evaluate_model, test_pred
from model_complet.model import predict_from_saved_model
from model_complet.model import build_fit_pipeline


if __name__ == '__main__':
    
    ######get data######
    df_today, df_yesterday = get_daily_db()
    
    #######preprocessing#######
    db = clean_data(df_today) 
    
    #########model########
    pipe, feature_name, X, y = build_fit_pipeline(db)
    evaluate_model(pipe, X, y) # bonus , vraiment pas obligatoire
    make_pred()
    predict_from_saved_model()
    predict_from_saved_model()
    
    # save_model()    #pour appeler le pikle
    # predict_from_saved_model()
    
    return 
