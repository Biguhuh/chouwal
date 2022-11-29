import math
import numpy as np
import pandas as pd
import pygeohash as gh

from taxifare.ml_logic.utils import simple_time_and_memory_tracker

def transform_time_features(X: pd.DataFrame) -> np.ndarray:

    assert isinstance(X, pd.DataFrame)
    pickup_dt = pd.to_datetime(X["pickup_datetime"],
                               format="%Y-%m-%d %H:%M:%S UTC",
                               utc=True)
    pickup_dt = pickup_dt.dt.tz_convert("America/New_York").dt
    dow = pickup_dt.weekday
    hour = pickup_dt.hour
    month = pickup_dt.month
    year = pickup_dt.year
    hour_sin = np.sin(2 * math.pi / 24 * hour)
    hour_cos = np.cos(2 * math.pi / 24 * hour)

    result = np.stack([hour_sin, hour_cos, dow, month, year], axis=1)
    return result
