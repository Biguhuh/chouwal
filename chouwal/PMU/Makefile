csv_to_df:
	python -c 'from pmu_breaking.ml_logic.data import to_df; to_df()'
	echo $$? > output.txt
clean_data:
	python -c 'from pmu_breaking.ml_logic.data import clean_data; clean_data()'

target_refine:
	python -c 'from pmu_breaking.ml_logic.model import scaling_imputing; scaling_imputing()'

features_target:
	python -c 'from pmu_breaking.ml_logic.model import define_features_target; define_features_target()'

scaling_imputing:
	python -c 'from pmu_breaking.ml_logic.model import scaling_imputing; scaling_imputing()'

initialize_model:
	python -c 'from pmu_breaking.ml_logic.model import initialize_model; initialize_model()'

train_model:
	python -c 'from pmu_breaking.ml_logic.model import train_model; train_model(); train_model()'

evaluate_model:
	python -c 'from pmu_breaking.ml_logic.model import evaluate_model; evaluate_model()'

run_pred:
	python -c 'from pmu_breaking.interface.main import predict; predict(X_test)'

save_model:
	python -c 'from pmu_breaking.ml_logic.model import save_model'

run_model: run_all

run_workflow:
	PREFECT__LOGGING__LEVEL=${PREFECT_LOG_LEVEL} python -m taxifare.flow.main

run_api:
	uvicorn pmu_breaking.api.fast:app --reload

####### TESTS #####
test_api:
test_api_root test_api_predict
