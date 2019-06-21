from stockklyApi.database.db import get_db


def get_price(ticker):
    db = get_db()['stockkly']
    prices_collection = db['prices']

    queryresult = prices_collection.find_one({"ticker": ticker.upper()})
    return queryresult


# def find_price(ticker, pdate):
#     db_conn = db['stockkly']
#     price_collection = db_conn['prices']
#     return price_collection.find_one({'ticker': ticker.upper(), 'priceDate': pdate})


# def get_price(ticker):
#     db = get_db()['stockkly']
#     prices_collection = db['prices']

#     queryresult = prices_collection.find_one({"ticker": ticker})
#     return queryresult


def create_price(data):
    db = get_db()['stockkly']
    price_collection = db['prices']

    queryresult = price_collection.find_one({"ticker": data['ticker'].upper()})

    if not queryresult:
        price = {
            "ticker": data['ticker'].upper(),
            "open":  data['open'],
            "price": data['price'],
            "change": data['change'],
            "movement": data['movement']
        }
        price_collection.insert_one(price)
    return


def upsert_price(data, id):
    db = get_db()['stockkly']
    price_collection = db['prices']

    price = {
        "ticker": data['ticker'].upper(),
        "open":  data['open'],
        "price": data['price'],
        "change": data['change'],
        "movement": data['movement']
    }
    return price_collection.update_one({'ticker': id.upper()}, {"$set": price}, upsert=True)
