# from stockklyApi.api import auth
from stockklyApi.database.db import get_db
# import json
# from bson import json_util
# from bson.objectid import ObjectId


def get(ticker):
    db = get_db()['stockkly']
    product_collection = db['products']

    queryresult = product_collection.find_one({"ticker": ticker})

    if not queryresult:
        product = {
            'ticker': ticker,
            'ccy': "USD",
            'symbol': "$"

        }
        return product
    # If new set-up an empty profile

    return queryresult
