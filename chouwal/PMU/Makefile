install_requirements:
	@pip install -r requirements.txt

pipeline_get_data:
	python -c 'from pmu_breaking.ml_logic.pipeline import get_data(); get_data()'

pipeline_processing:
	python -c 'from pmu_breaking.ml_logic.pipeline import final_preprocessing(); final_preprocessing()'

csv_to_df:
	python -c 'from pmu_breaking.ml_logic.data import to_df; to_df()'
	echo $$? > output.txt

clean_data:
	python -c 'from pmu_breaking.ml_logic.data import clean_data; clean_data()'

drop_non_french_races:
	python -c 'from pmu_breaking.ml_logic.pipeline import drop_non_french_races; drop_non_french_races()'

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

predictions:
	python -c 'from pmu_breaking.ml_logic.model import predict; predict()'

save_model:
	python -c 'from pmu_breaking.ml_logic.model import save_model; save_model()'

load_model:
	python -c 'from pmu_breaking.ml_logic.model import load_model; load_model()'

lucas_read:
	python -c 'from pmu_breaking.ml_logic.lucas_preprocessor import read_raw_data; read_raw_data()'

lucas_perc_nans:
	python -c 'from pmu_breaking.ml_logic.lucas_preprocessor import columns_percentage_nan; columns_percentage_nan()';

lucas_create_y:
	python -c 'from pmu_breaking.ml_logic.lucas_preprocessor import create_y; create_y()';

lucas_raced:
	python -c 'from pmu_breaking.ml_logic.lucas_preprocessor import raced_races; raced_races()';

lucas_non_raced:
	python -c 'from pmu_breaking.ml_logic.lucas_preprocessor import non_raced_races; non_raced_races()';

lucas_compare_races:
	python -c 'from pmu_breaking.ml_logic.lucas_preprocessor import compare_raced_nonraced_size; compare_raced_nonraced_size()';

lucas_drop_useless:
	python -c 'from pmu_breaking.ml_logic.lucas_preprocessor import not_numeric; not_numeric()';

lucas_preprocess:
	python -c 'from pmu_breaking.ml_logic.lucas_preprocessor import preprocess; preprocess()';

run_workflow:
	PREFECT__LOGGING__LEVEL=${PREFECT_LOG_LEVEL} python -m taxifare.flow.main

run_api:
	uvicorn pmu_breaking.api.fast:app --reload

####### TESTS #####
test_api:
	test_api_root test_api_predict

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr chouwal-*.dist-info
	@rm -fr chouwal.egg-info
