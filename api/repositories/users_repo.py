from api.mongo import mongoDB


def get_user(user_id):
    queryresult = mongoDB.db.users.find_one({"userId": user_id})
    return queryresult


def create_user(data, user_id):
    queryresult = mongoDB.db.users.find_one({"userId": user_id})

    if not queryresult:
        user = {
            "userId": user_id,
            "watchList": data['watchList'],
            "currency": data['currency'],
            "symbol": data['symbol'],
            "refreshRate": data['refreshRate'],
            "devmode": False
        }
        mongoDB.db.users.insert_one(user)
    return


def upsert_user(data, user_id):
    user = {
        "watchList": data['watchList'],
        "currency": data['currency'],
        "symbol": data['symbol'],
        "refreshRate": data['refreshRate'],
        "devmode": data['devmode']
    }
    return mongoDB.db.users.update_one({'userId': user_id}, {"$set": user}, upsert=True)
