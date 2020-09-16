from bson import json_util
from bson.objectid import ObjectId
from api.mongo import mongoDB


def get_transaction_history_for_user_and_product(user_id, ticker):
    queryresult = mongoDB.db.transactions.find({"owner": user_id, "ticker": ticker.upper()})
    return queryresult


def get_transaction_history_for_user(user_id):
    queryresult = mongoDB.db.transactions.find({"owner": user_id})

    json_results = json_util.dumps(queryresult)
    return(json_results)


def get_transaction_by_id(id):
    resval = mongoDB.db.transactions.find_one({"_id": ObjectId(id)})
    return(resval)


def create_transaction(data, user_id):
    trans = {
        "owner": user_id,
        'ticker': data['ticker'].upper(),
        'transdate': data['transdate'],
        'transtype': data['transtype'],
        'quantity': float(data['quantity']),
        'price': float(data['price']),
        'details': data['details'],
    }
    return mongoDB.db.transactions.insert_one(trans)


def upsert_transaction(data, user_id):
    mongoId = ObjectId(data['id'])

    trans = {
        "owner": user_id,
        'ticker': data['ticker'].upper(),
        'transdate': data['transdate'],
        'transtype': data['transtype'],
        'quantity': float(data['quantity']),
        'price': float(data['price']),
        'details': data['details'],
    }
    return mongoDB.db.transactions.update_one({'_id': mongoId}, {"$set": trans}, upsert=True)


def delete_transaction(id):
    return mongoDB.db.transactions.delete_one({'_id': ObjectId(id)})
