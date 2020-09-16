from api.mongo import mongoDB


def get_balance(user_id, ticker):
    queryresult = mongoDB.db.balances.find_one({"userId": user_id, "ticker": ticker})
    return(queryresult)


def get_balances(user_id):
    return mongoDB.db.balances.find({"userId": user_id})


def create_balance(user_id, data):
    balance = {
        'ticker': data['ticker'],
        'userId': user_id,
        'qty': data['qty']
    }
    return mongoDB.db.balances.insert_one(balance)


def update_balance(user_id, ticker, qty):
    return mongoDB.db.balances.update_one({'ticker': ticker, "userId": user_id}, {"$set": {"qty": qty}}, upsert=True)
