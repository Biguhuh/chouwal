#from pmu_breaking.ml_logic.Model1.v1_edouard_preprocessing import to_df, clean_data, refining_target, define_features_target, scaling_imputing
#from pmu_breaking.ml_logic.Model1.model import test_pred,initialize_model, train_model, evaluate_model, test_pred
#from pmu_breaking.ml_logic.Model1.model import predict_from_saved_model
from pmu_breaking.ml_logic.Model1.model import build_fit_pipeline


if __name__ == '__main__':
    '''
    to_df()
    clean_data()
    refining_target()
    define_features_target()
    scaling_imputing()
    initialize_model()
    '''
    build_fit_pipeline()
    '''
    train_model()
    evaluate_model()
    test_pred()
    predict_from_saved_model()
    predict_from_saved_model()
    # save_model()
    # predict_from_saved_model()
    '''
