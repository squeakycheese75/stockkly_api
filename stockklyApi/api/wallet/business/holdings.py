
from stockklyApi.api import auth
from stockklyApi.database.db import get_db

from stockklyApi.api.wallet.business import prices
from stockklyApi.api.wallet.business import product
# import json
from bson import json_util
# from bson.objectid import ObjectId


# Increase ÷ Original Number × 100.
def calc_movement(increase, price):
    return (increase / price) * 100


def calc_total_change(holding, change):
    return (holding * change)


def calc_total(holding, price):
    return (holding * price)


def calc_change(price, open):
    return (price - open)


def get_holdings(userId):
    # get holdings
    db = get_db()['stockkly']
    holdings_collection = db['holdings']

    json_results = []
    queryresult = holdings_collection.find({"owner": userId})

    # json_results = json_util.dumps(queryresult)
    if queryresult.count() == 0:
        # if json_results is None:
        json_results = [{
            'ticker': "MSFT",
            'userId': 'james_wooltorton@hotmail.com',
            'qty': 150
        }]
    else:
        json_results = json_util.dumps(queryresult)

    # enrich with latest price
    for i in json_results:
        # enrich_price()
        price = prices.get(i['ticker'])
        # enrich
        change = calc_change(price['price'], price['open'])
        i['change'] = change
        i['price'] = price['price']
        i['movement'] = calc_movement(change, price['price'])
        i['total_change'] = calc_total_change(i['qty'], change)
        i['total'] = calc_total(i['qty'], price['price'])

        # product = product.get(i['ticker'])
        # Might do once at ui level...
        i['spot'] = 1.2922
        i['ccy'] = "USD"
        i['symbol'] = "$"

        i['name'] = 'Microsoft Ltd'
    # print(json_results)
    # enrich with asses data

    return json_results


# h1 = {
#     'ticker': "MSFT",
#     'name': "Microsoft Ltd",
#     'change': 0.19,
#     'price': 123.37,
#     'movement': 2.10,
#     'total_change': 300.66,
#     'qty': 150,
#     'total': 18505.00,
#     'spot': 1.2922,
#     'ccy': "USD",
#     'symbol': "$"
# }
# h2 = {
#     'ticker': "BTC-USD",
#     'name': "Bitcoin",
#     'change': 0.19,
#     'price': 5272.76,
#     'movement': 0.76,
#     'total_change': 300.66,
#     'qty': 8.99,
#     'total': 47434.02,
#     'spot': 1.2922,
#     'ccy': "USD",
#     'symbol': "$"
# }
# h3 = {
#     'ticker': "GOLD-OZ",
#     'name': "Gold Oz",
#     'change': -0.19,
#     'price': 982.17,
#     'movement': -1.10,
#     'total_change': -300.66,
#     'qty': 6,
#     'total': 5893.02,
#     'spot': 1,
#     'ccy': "GBP",
#     'symbol': "£"
# }
# response = [h1, h2, h3]
