from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pmu_breaking.interface.main import pred
from pmu_breaking.ml_logic.registry import load_model
from pmu_breaking.ml_logic.preprocessor import preprocess_features

app = FastAPI()
app.state.model = load_model()

@app.get("/predict_one")
def predict_winner():
    return {'Winner': str(y_pred[0]) }

@app.get("/predict_one_gains")
def predict_winner_gains():
    return {'Gains with winner' : int(y_pred) }

@app.get("/predict_three")
def predict_three_winners():
    return {'3 winners' : str(y_pred)}

@app.get("/predict_three_gains")
def predict_three_winners_gains():
    return {'Gains with 3 winners': int(y_pred)}
