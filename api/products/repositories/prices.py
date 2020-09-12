from api.mongo import mongoDB
import datetime


def get_price_latest(ticker):
    # queryresult = mongoDB.db.prices.find({"ticker": ticker.upper()}).sort({"priceDate": -1}).limit(1)
    # queryresult = mongoDB.db.prices.find_one({"ticker":  ticker.upper()}).sort('priceDate', -1)
    queryresult = mongoDB.db.prices.find_one(
        {'ticker': ticker.upper()},
        sort=[('priceDate', -1)]
    )
    return queryresult


def get_price_now(ticker):
    price_date = datetime.datetime.strptime(
        str(datetime.datetime.now().date()), "%Y-%m-%d")
    return mongoDB.db.prices.find_one({'ticker': ticker.upper(), 'priceDate': price_date})


def get_price(ticker, price_date):
    price_date = datetime.datetime.strptime(
        price_date, "%Y-%m-%d")
    return mongoDB.db.prices.find_one({'ticker': ticker.upper(), 'priceDate': price_date})


def get_price_previous(ticker, price_date):
    queryresult = mongoDB.db.prices.find_one({'ticker':  ticker.upper(), 'priceDate': {'$lt': price_date}},  sort=[('priceDate', -1)])
    return queryresult


def get_prices(self, ticker):
    return mongoDB.db.prices.find({'ticker': ticker.upper()})


def get_price_trend(ticker, limit):
    queryresult = mongoDB.db.prices.find(
        {'ticker': ticker.upper()},
        {'_id': 0, 'price': 1, 'priceDate': 1},
        sort=[('priceDate', -1)],
        limit=limit
    )
    return queryresult


# def create_price(data):
#     queryresult = mongoDB.db.prices.find_one({"ticker": data['ticker'].upper()})

#     if not queryresult:
#         price = {
#             "ticker": data['ticker'].upper(),
#             "open":  data['open'],
#             "price": data['price'],
#             "change": data['change'],
#             "movement": data['movement']
#         }
#         mongoDB.db.prices.insert_one(price)
#     return


# def upsert_price(data, id):
#     # db = get_db()['stockkly']
#     # price_collection = db['prices']

#     price = {
#         "ticker": data['ticker'].upper(),
#         "open":  data['open'],
#         "price": data['price'],
#         "change": data['change'],
#         "movement": data['movement']
#     }
#     return mongoDB.db.prices.update_one({'ticker': id.upper()}, {"$set": price}, upsert=True)
