# Version v1 - Edouard preprocessing - Simple Logistic Regression
csv_to_df:
	python -c 'from pmu_breaking.ml_logic.Model1.v1_edouard_preprocessing import to_df; to_df()'
	echo $$? > output.txt

clean_data:
	python -c 'from pmu_breaking.ml_logic.data.Model1.v1_edouard_preprocessing import clean_data; clean_data()'

target_refine:
	python -c 'from pmu_breaking.ml_logic.model.Model1.v1_edouard_preprocessing import scaling_imputing; scaling_imputing()'

features_target:
	python -c 'from pmu_breaking.ml_logic.model.Model1.v1_edouard_preprocessing import define_features_target; define_features_target()'

scaling_imputing:
	python -c 'from pmu_breaking.ml_logic.model.Model1.v1_edouard_preprocessing import scaling_imputing; scaling_imputing()'

initialize_model:
	python -c 'from pmu_breaking.ml_logic.model.Model1.model import initialize_model; initialize_model()'

train_model:
	python -c 'from pmu_breaking.ml_logic.model.Model1.model import train_model; train_model(); train_model()'

evaluate_model:
	python -c 'from pmu_breaking.ml_logic.model.Model1.model import evaluate_model; evaluate_model()'

predictions:
	python -c 'from pmu_breaking.ml_logic.model.Model1.model import predict; predict()'

save_model:
	python -c 'from pmu_breaking.ml_logic.model.Model1.model import save_model; save_model()'

load_model:
	python -c 'from pmu_breaking.ml_logic.model.Model1.model import load_model; load_model()'

# Run WebApp
streamlit:
	-@streamlit run app.py
