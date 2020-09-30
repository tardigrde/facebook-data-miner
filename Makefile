lint:
	pipenv run isort miner
	pipenv run black .
	pipenv run flake8
	pipenv run mypy .

lint-test:
	pipenv run isort miner --check-only
	pipenv run flake8
	pipenv run mypy .

test: lint-test
	coverage run
	coverage report

