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
	echo "MONGO_URI=mongodb://localhost:27017" >> .env
	echo "FLASK_APP=stockklyAPI" >> .flaskenv
	echo "FLASK_ENV=development" >> .flaskenv
	echo "FLASK_RUN_PORT=8080" >> .flaskenv

dependancies: 
	pip3 install -r requirements/base.txt 

flake8:
	flake8 ./api/prices
	flake8 ./api/products
	flake8 ./api/profile
	flake8 ./api/wallet
	flake8 ./api/watchlist

test-requirements:
	pip3 install -r requirements/test.txt

test-unit: test-requirements
	pytest --cov=./api/products --cov-fail-under 70 --cov-report term-missing --cov-report xml tests/unit/ -v