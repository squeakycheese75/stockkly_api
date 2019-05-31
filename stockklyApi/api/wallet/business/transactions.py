
from stockklyApi.api import auth
from stockklyApi.database.db import get_db
import json
from bson import json_util
from bson.objectid import ObjectId

# from bson.json_util import dumps

import datetime


def get_transaction_history_for_user_and_product(userId, ticker):
    db = get_db()['stockkly']
    user_collection = db['transactions']

    queryresult = user_collection.find({"owner": userId, "ticker": ticker})
    json_results = json_util.dumps(queryresult)
    return json_results


def get_transaction_history_for_user(userId):
    db = get_db()['stockkly']
    user_collection = db['transactions']

    queryresult = user_collection.find({"owner": userId})

    json_results = json_util.dumps(queryresult)
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
