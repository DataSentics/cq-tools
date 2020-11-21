help: 
	@echo "---------------HELP-----------------"
	@echo " - make check-errors (check for possible errors)"
	@echo " - make check-warnings (check for best practices)"
	@echo " - make test (execute unit tests)"
	@echo " - make build (build package)"
	@echo " - make testpackage (build package and execute tests)"
	@echo "------------------------------------"

test: 
	poetry run bash -c "export ADF_PIPELINE_PATH="tests/test_files/src" && poetry run python -m pytest"	
build: 
	poetry build