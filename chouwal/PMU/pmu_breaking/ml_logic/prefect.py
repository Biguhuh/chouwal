from taxifare_model.interface.main import (preprocess, train, evaluate)
from prefect import task

@task
def eval_perf(next_row):
    past_perf = evaluate(next_row)
    return past_perf
@task
def train_model(next_row):
    preprocess(first_row=next_row)
    new_perf = train(first_row=next_row, stage="Production")
    return new_perf

@task
def notify(past_perf, new_perf):
    print(f"Past perf: {past_perf}, new perf: {new_perf}")
