from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pmu_breaking.ml_logic.Model1.model import predict_from_saved_model
import pandas as pd
from Model1.model import load_model

app = FastAPI()
app.state.model = load_model()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def root():
    return {'greeting': 'Hello, are you looking for the best three horses in upcoming PMU race ?'}

'''
app = FastAPI()
app.state.model = ...

@app.get("/predict")
...
app.state.model.predict(...)
'''
