from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pmu_breaking.ml_logic.Model1.model import predict_from_saved_model
import pandas as pd
from taxifare.ml_logic.registry import load_model
from taxifare.ml_logic.preprocessor import preprocess_features

app = FastAPI()
app.state.model = load_model()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# http://127.0.0.1:8000/predict?pickup_datetime=2012-10-06?12:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2
@app.get("/predict")
def predict(data):      # 1
    """
    we use type hinting to indicate the data types expected
    for the parameters of the function
    FastAPI uses this information in order to hand errors
    to the developpers providing incompatible parameters
    FastAPI also provides variables of the expected data type to use
    without type hinting we need to manually convert
    the parameters of the functions which are all received as strings
    """

    X_pred = pd.DataFrame(dict(
            key=pickup_datetime,  # useless but the pipeline requires it
            pickup_datetime=[pickup_datetime],
            pickup_longitude=[pickup_longitude],
            pickup_latitude=[pickup_latitude],
            dropoff_longitude=[dropoff_longitude],
            dropoff_latitude=[dropoff_latitude],
            passenger_count=[passenger_count]
        ))

    predicted = predict_from_saved_model(X_pred)

    X_processed = preprocess_features(X_pred)
    y_pred = app.state.model.predict(X_processed)
    print('Three winners : \n')
    print(f'Three winners:\n Winner: {y_pred[0]}\n Second: {y_pred[1]}\n Third: {y_pred[2]}\n')
    return { 'Winner' : {y_pred[0]} }

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
