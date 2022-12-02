install_requirements:
	@pip install -r requirements.txt

# Prefect
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
