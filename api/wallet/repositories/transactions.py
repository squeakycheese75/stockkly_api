
from api import auth
# from database.db import get_db
import json
from bson import json_util
from bson.objectid import ObjectId
from mongo import mongoDB


# from bson.json_util import dumps

import datetime


def get_transaction_history_for_user_and_product(userId, ticker):
    # db = get_db()['stockkly']
    # user_collection = db['transactions']

    queryresult = mongoDB.db.transactions.find({"owner": userId, "ticker": ticker.upper()})
    json_results = json_util.dumps(queryresult)
    return json_results


def get_transaction_history_for_user(userId):
    # db = get_db()['stockkly']
    # user_collection = db['transactions']

    queryresult = mongoDB.db.transactions.find({"owner": userId})

    json_results = json_util.dumps(queryresult)
    return(json_results)


def create_transaction(data, userId):
    # db = get_db()['stockkly']
    # transactionsCollection = db['transactions']

    # handle empty lists
    trans = {
        "owner": userId,
        'ticker': data['ticker'].upper(),
        'transdate': data['transdate'],
        'transtype': data['transtype'],
        'quantity': data['quantity'],
        'price': data['price'],
        'details': data['details'],
    }
    return mongoDB.db.transactions.insert_one(trans)


def upsert_transaction(data, userId):
    # db = get_db()['stockkly']
    # trans_collection = db['transactions']
    mongoId = data['_id']

    trans = {
        "owner": userId,
        'ticker': data['ticker'].upper(),
        'transdate': data['transdate'],
        'transtype': data['transtype'],
        'quantity': data['quantity'],
        'price': data['price'],
        'details': data['details'],
    }
    return mongoDB.db.transactions.update_one({'_id': mongoId}, {"$set": trans}, upsert=True)
