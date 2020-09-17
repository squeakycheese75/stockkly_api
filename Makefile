define HELP

Usage:

make create-local-env           - Create skeleton .env file.
make dependancies               - Install base dependancies.
make flake8                     - Run flake8 linting.
make test-unit                  - Run unit tests.

endef

export HELP

create-local-env:
	echo "MONGO_CONNECTION=mongodb://localhost:27017/stockkly" >> .env
	echo "AUTH0_DOMAIN=***your autho0 domain crdentials***" >> .env
	echo "API_IDENTIFIER=***your front end***" >> .env
	echo "FLASK_APP=stockklyAPI" >> .flaskenv
	echo "FLASK_ENV=development" >> .flaskenv
	echo "FLASK_RUN_PORT=5000" >> .flaskenv
	echo "FLASK_DEBUG=True" >> .flaskenv

dependancies: 
	pip3 install -r requirements/base.txt 

flake8:
	flake8 ./api/controllers
	flake8 ./api/endpoints
	flake8 ./api/repositories
	flake8 ./api/shared
	flake8 app.py

test-requirements:
	pip3 install -r ./api/requirements/test.txt

test-unit:
	pytest --cov=./api/controllers --cov=./api/shared --cov-fail-under 70 --cov-report term-missing --cov-report xml tests/unit/ -v

commit: flake8
	cz commit