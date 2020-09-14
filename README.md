# Stockkly API

StockklyAPI is a free, near real-time, RestAPI for providing prices for stocks (FTSE100, NASDAQ), crypto-currencies (BTC), funds and precious metals (e.g. GOLD, SILVER).

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=squeakycheese75_stockklyApi&metric=alert_status)](https://sonarcloud.io/dashboard?id=squeakycheese75_stockklyApi)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=squeakycheese75_stockklyApi&metric=bugs)](https://sonarcloud.io/dashboard?id=squeakycheese75_stockklyApi)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=squeakycheese75_stockklyApi&metric=security_rating)](https://sonarcloud.io/dashboard?id=squeakycheese75_stockklyApi)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=squeakycheese75_stockklyApi&metric=sqale_index)](https://sonarcloud.io/dashboard?id=squeakycheese75_stockklyApi)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=squeakycheese75_stockklyApi&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=squeakycheese75_stockklyApi)


## Exchanges

* FTSE

## Sectors

* Fiat
* Crypto
* Precious Metals
* Funds
* Stock

## Usage


## Dependancies

The below are dependancies for the StockklyAPI.  

* [MongoDb installed](https://hub.docker.com/_/mongo)

These can be constructed via the docker:

1. Ensure you have docker installed. 
2. ```cd dependancies```
3. ```docker-compose up -d```

## Hosting

Currently hosted at: <https://stockklyapi.azurewebsites.net/api/>

## Getting Started
1. Set up your local environment using ```make create-local-env```
2. Update your local environment details
3. ```run flask```

## Disclaimer

StockkyAPI is an open source project for collating and provide data from various sources, despite best attempts data provided is not be suitable 
for making decisions and should be considered as test.  Stockkly also does not gurantee that the data is live. 
