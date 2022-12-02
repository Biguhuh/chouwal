# Version v3 - Last processing
pipeline_get_data:
	python -c 'from pmu_breaking.ml_logic.Model3.v3_pipeline import get_data(); get_data()'

pipeline_processing:
	python -c 'from pmu_breaking.ml_logic.Model3.v3_pipeline import final_preprocessing(); final_preprocessing()'

drop_non_french_races:
	python -c 'from pmu_breaking.ml_logic.Model3.v3_pipeline import drop_non_french_races; drop_non_french_races()'
