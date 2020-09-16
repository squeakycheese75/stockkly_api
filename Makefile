define HELP

Usage:

make create-local-env           - Create skeleton .env file.
make dependancies               - Install base dependancies.
make flake8                     - Run flake8 linting.
make test-unit                  - Run unit tests.

endef

export HELP

create-local-env:
	echo "MONGO_CONNECTION=stockkly" >> .env
	echo "FLASK_APP=stockklyAPI" >> .flaskenv
	echo "FLASK_ENV=development" >> .flaskenv
	echo "FLASK_RUN_PORT=5000" >> .flaskenv
	echo "FLASK_DEBUG=True" >> .flaskenv

dependancies: 
	pip3 install -r requirements/base.txt 

flake8:
	flake8 ./api/business
	flake8 ./api/endpoints
	flake8 ./api/repositories
	# flake8 ./tests

test-requirements:
	pip3 install -r requirements/test.txt

test-unit:
	pytest --cov=./api/business --cov-fail-under 70 --cov-report term-missing --cov-report xml tests/unit/ -v