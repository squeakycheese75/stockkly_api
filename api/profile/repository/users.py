from mongo import mongoDB


def get_user(userId):
    queryresult = mongoDB.db.users.find_one({"userId": userId})
    return queryresult


def create_user(data, userId):
    queryresult = mongoDB.db.users.find_one({"userId": userId})

    if not queryresult:
        user = {
            "userId": userId,
            "watchList": data['watchList'],
            "currency": data['currency'],
            "symbol": data['symbol'],
            "refreshRate": data['refreshRate'],
            "devmode": False
        }
        mongoDB.db.users.insert_one(user)
    return


def upsert_user(data, userId):
    user = {
        "watchList": data['watchList'],
        "currency": data['currency'],
        "symbol": data['symbol'],
        "refreshRate": data['refreshRate'],
        "devmode": data['devmode']
    }
    return mongoDB.db.users.update_one({'userId': userId}, {"$set": user}, upsert=True)
