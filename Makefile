help: 
	@echo "---------------HELP-----------------"
	@echo " - make check-errors (check for possible errors)"
	@echo " - make check-warnings (check for best practices)"
	@echo " - make test (execute unit tests)"
	@echo "------------------------------------"

test: 
	poetry run python -m pytest -s

testpackage: 
	make build && \
	poetry run bash -c "cd tests && poetry update cqtools" && \
	make test

build: 
	poetry build

check-errors:
	poetry run pre-commit run -a error

check-warnings:
	poetry run pre-commit run -a warning