import json
from bson import json_util
from mongo import mongoDB


def get_product(ticker):
    queryresult = mongoDB.db.products.find_one({"ticker": ticker.upper()})
    return queryresult


def get_sectors():
    queryresult = mongoDB.db.products.distinct('sector')
    # queryresult = mongoDB.db.products.distinct("sector").sort(1)
    return queryresult


def get_products():
    queryresult = mongoDB.db.products.find({})
    json_results = json_util.dumps(queryresult)
    return json_results


def create_product(data):
    queryresult = mongoDB.db.products.find_one({"ticker": data['ticker'].upper()})

    if not queryresult:
        product = {
            "ticker": data['ticker'].upper(),
            "displayTicker":  data['displayTicker'],
            "name": data['name'],
            "description": data['description'],
            "company": data['company'],
            "sector": data['sector'],
            "quote": data['quote'],
            "exchange": data['exchange']
        }
        mongoDB.db.products.insert_one(product)
    return


def upsert_product(data, ticker):
    product = {
        "ticker": data['ticker'].upper(),
        "displayTicker":  data['displayTicker'],
        "name": data['name'],
        "description": data['description'],
        "company": data['company'],
        "sector": data['sector'],
        "quote": data['quote'],
        "exchange": data['exchange']
    }
    return mongoDB.db.products.update_one({'ticker': ticker.upper()}, {"$set": product}, upsert=True)
