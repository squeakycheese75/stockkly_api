# from stockklyApi.api import auth
from stockklyApi.database.db import get_db
# import json
# from bson import json_util
# from bson.objectid import ObjectId


def get_product(id):
    db = get_db()['stockkly']
    product_collection = db['products']

    queryresult = product_collection.find_one({"ticker": id})

    if not queryresult:
        response = {
            "ticker": "BTC-USD",
            "displayTicker": "BTC:USD",
            "name": "Bitcoin (USD)",
            "description": "Bitcoin is an experimental digital currency that enables instant payments to anyone, anywhere in the world.",
            "company": {
                    "name": "Bitcoin",
                    "url": "https://bitcoin.org/"
            },
            "sector": "Crypto",
            # "exchanges": ["CPRO"],
            "quote": {
                "symbol": "$",
                "currency": "USD"
            }
        }
        return response
    # If new set-up an empty profile

    return queryresult


# def create_product(data):
#     db = get_db()['stockkly']
#     product_collection = db['products']

#     queryresult = product_collection.find_one({"ticker": data['ticker']})

#     if not queryresult:
#         product = {
#             "ticker": data['ticker'],
#             "displayTicker":  data['displayTicker'],
#             "name": data['name'],
#             "description": data['description'],
#             "company": data['company'],
#             "sector": data['sector'],
#             "quote": data['quote']
#         }
#         product_collection.insert_one(product)
#     return


def upsert_product(data):
    db = get_db()['stockkly']
    product_collection = db['products']

    product = {
        "ticker": data['ticker'],
        "displayTicker":  data['displayTicker'],
        "name": data['name'],
        "description": data['description'],
        "company": data['company'],
        "sector": data['sector'],
        "quote": data['quote']
    }
    return product_collection.update_one({'ticker': data['ticker']}, {"$set": product}, upsert=True)
