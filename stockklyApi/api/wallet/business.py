
from stockklyApi.api import auth
from stockklyApi.database.db import get_db
import json
from bson import json_util
from bson.objectid import ObjectId

# from bson.json_util import dumps

import datetime


def get_holdings():
    h1 = {
        'ticker': "MSFT",
        'name': "Microsoft Ltd",
        'change': 0.19,
        'price': 123.37,
        'movement': 2.10,
        'qty': 150,
        'total': 18505.00,
        'spot': 1.2922,
        'ccy': "USD"
    }
    h2 = {
        'ticker': "BTC-USD",
        'name': "Bitcoin",
        'change': 0.19,
        'price': 5272.76,
        'movement': 0.76,
        'qty': 8.99,
        'total': 47434.02,
        'spot': 1.2922,
        'ccy': "USD"
    }
    h3 = {
        'ticker': "GOLD-OZ",
        'name': "Gold Oz",
        'change': -0.19,
        'price': 982.17,
        'movement': -1.10,
        'qty': 6,
        'total': 5893.02,
        'spot': 1,
        'ccy': "GBP"
    }
    response = [h1, h2, h3]
    return response


def get_transaction_history_for_user_and_product(userId, ticker):
    db = get_db()['stockkly']
    user_collection = db['transactions']

    queryresult = user_collection.find({"owner": userId, "ticker": ticker})
    json_results = json_util.dumps(queryresult)
    # docs_list = list(queryresult)
    # return json.dumps(docs_list, default=json_util.default)
    # json_results = []
    # for result in queryresult:
    #     json_results.append(result)
    # return json_util.dumps(json_results)
    # print(json_results)
    return json_results


def get_transaction_history_for_user(userId):
    db = get_db()['stockkly']
    user_collection = db['transactions']

    queryresult = user_collection.find({"owner": userId})

    json_results = dumps(queryresult)
    return(json_results)


def create_transaction(data):
    userEmail = auth.get_userinfo_with_token()['email']

    db = get_db()['stockkly']
    transactionsCollection = db['transactions']

    # handle empty lists
    trans = {
        "owner": userEmail,
        'ticker': data['ticker'],
        'transdate': data['transdate'],
        'transtype': data['transtype'],
        'quantity': data['quantity'],
        'price': data['price'],
        'details': data['details'],
    }
    return transactionsCollection.insert_one(trans)
