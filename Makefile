help: 
	@echo "---------------HELP-----------------"
	@echo " - make check-errors (check for possible errors)"
	@echo " - make check-warnings (check for best practices)"
	@echo " - make test (execute unit tests)"
	@echo "------------------------------------"

test:
	python checks/tests.py

check-errors:
	pre-commit run -a error

check-warnings:
	pre-commit run -a warning