
from stockklyApi.api import auth
from stockklyApi.database.db import get_db

# from stockklyApi.api.wallet.business import prices

from bson import json_util


def get_balance(userId, ticker):
    db = get_db()['stockkly']
    holdingCollection = db['balances']
    queryresult = holdingCollection.find_one({"userId": userId, "ticker": ticker})
    # json_results = json_util.dumps(queryresult)
    return(queryresult)


def get_balances(userId):
    db = get_db()['stockkly']
    holdingCollection = db['balances']
    return holdingCollection.find({"userId": userId})


def create_balance(userEmail, data):
    db = get_db()['stockkly']
    holdingCollection = db['balances']

    balance = {
        'ticker': data['ticker'],
        'userId': userEmail,
        'qty': data['qty']
    }
    return holdingCollection.insert_one(balance)


def update_balance(userEmail, ticker, qty):
    db = get_db()['stockkly']
    product_collection = db['balances']
    return product_collection.update_one({'ticker': ticker, "userId": userEmail}, {"$set": {"qty": qty}}, upsert=True)
