from stockklyApi.database.db import get_db


def get_user(userId):
    db = get_db()['stockkly']
    prices_collection = db['users']

    queryresult = prices_collection.find_one({"userId": userId.lower()})
    return queryresult
