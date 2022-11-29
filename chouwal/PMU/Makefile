reinstall_package:
	@pip uninstall -y pmu_breaking || :

run_preprocess:
	python -c 'from taxifare.interface.main import preprocess; preprocess(); preprocess(source_type="val")'

run_train:
	python -c 'from pmu_breaking.interface.main import train; train()'

run_pred:
	python -c 'from pmu_breaking.interface.main import predict; predict()'

run_evaluate:
	python -c 'from pmu_breaking.interface.main import evaluate; evaluate()'

run_all:
	run_preprocess run_train run_pred run_evaluate

run_model: run_all

run_workflow:
	PREFECT__LOGGING__LEVEL=${PREFECT_LOG_LEVEL} python -m taxifare.flow.main

run_api:
	uvicorn taxifare.api.fast:app --reload

####### TESTS #####
test_api: test_api_root test_api_predict
