import numpy as np
import pandas as pd
from pmu_breaking.ml_logic.data import to_df, clean_data
from sklearn.linear_model import LogisticRegression
# from pmu_breaking.ml_logic.model import initialize_model, compile_model, train_model, evaluate_model
#from pmu_breaking.ml_logic.params import CHUNK_SIZE, DATASET_SIZE, VALIDATION_DATASET_SIZE
#from pmu_breaking.ml_logic.preprocessor import preprocess_features
#from pmu_breaking.ml_logic.utils import get_dataset_timestamp
#from pmu_breaking.ml_logic.registry import get_model_version
#from pmu_breaking.ml_logic.registry import load_model, save_model

def train():
    """
    Train a new model on the full (already preprocessed) dataset ITERATIVELY, by loading it
    chunk-by-chunk, and updating the weight of the model after each chunks.
    Save final model once it has seen all data, and compute validation metrics on a holdout validation set
    common to all chunks.
    """
    model = build_model()
    print("\n Model built 🫡")
    # X =
    # y =
    model.fit(X, y)
    print("\n Model fit 🫡")

    return model

def evaluate():
    model = train()
    if model is None:
        print("There's no model, maybe there was a pb with building the model ?")
        return
    print(f'Model score : {model.score}')
    return model.score

def pred(X_pred: pd.DataFrame = None) -> np.ndarray:
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

if __name__ == '__main__':
    to_df()
    clean_data()
    train()
    pred()
    evaluate()
