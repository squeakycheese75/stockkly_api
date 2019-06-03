# from stockklyApi.api import auth
from stockklyApi.database.db import get_db
# import json
# from bson import json_util
# from bson.objectid import ObjectId


def get(ticker):
    db = get_db()['stockkly']
    prices_collection = db['prices']

    queryresult = prices_collection.find_one({"ticker": ticker})

    if not queryresult:
        price = {
            'open': 123.18,
            'price': 123.37
            # 'change' = 0.19,
            # 'movement' = 2.10,
            # 'total_change' = 300.66,
            # 'total' = 18505.00,
            # 'spot' = 1.2922,
            # 'ccy' = "USD"
            # 'symbol' = "$"
        }
        return price
    # If new set-up an empty profile

    return queryresult
