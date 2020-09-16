from api.mongo import mongoDB
import datetime


def get_price_latest(ticker):
    queryresult = mongoDB.db.prices.find_one(
        {'ticker': ticker.upper()},
        sort=[('priceDate', -1)]
    )
    return queryresult


def get_price_now(ticker):
    price_date = datetime.datetime.strptime(
        str(datetime.datetime.now().date()), "%Y-%m-%d")
    return mongoDB.db.prices.find_one({'ticker': ticker.upper(), 'priceDate': price_date})


def get_price(ticker, price_date):
    price_date = datetime.datetime.strptime(
        price_date, "%Y-%m-%d")
    return mongoDB.db.prices.find_one({'ticker': ticker.upper(), 'priceDate': price_date})


def get_price_previous(ticker, price_date):
    queryresult = mongoDB.db.prices.find_one({'ticker':  ticker.upper(), 'priceDate': {'$lt': price_date}},  sort=[('priceDate', -1)])
    return queryresult


def get_prices(self, ticker):
    return mongoDB.db.prices.find({'ticker': ticker.upper()})


def get_price_trend(ticker, limit):
    queryresult = mongoDB.db.prices.find(
        {'ticker': ticker.upper()},
        {'_id': 0, 'price': 1, 'priceDate': 1},
        sort=[('priceDate', -1)],
        limit=limit
    )
    return queryresult
