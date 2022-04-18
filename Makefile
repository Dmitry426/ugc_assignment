.PHONY: dev pre-commit isort black mypy flake8 pylint lint

dev: pre-commit

pre-commit:
	pre-commit install
	pre-commit autoupdate

isort:
	isort . --profile black

black:
	black .

mypy:
	mypy -p ugc_service

flake8:
	flake8 .

pylint:
	pylint etl_events ugc_service tests

lint: isort black mypy flake8 pylint

.PHONY: test
test:
	docker-compose -f tests/docker-compose.yml down --remove-orphans
	docker-compose -f tests/docker-compose.yml run test


.PHONY: test-cleanup
test-cleanup:
	docker-compose -f tests/docker-compose.yml down
