
from stockklyApi.api import auth
from stockklyApi.database.db import get_db

from stockklyApi.api.wallet.repositories import balances
from stockklyApi.api.products.repositories import products, prices
# from stockklyApi.api.wallet.business import product

from bson import json_util
# from bson.objectid import ObjectId

# need some tests....:)
# Increase ÷ Original Number × 100.


def calc_movement(increase, price):
    return (increase / price) * 100


def calc_total_change(holding, change):
    return (holding * change)


def calc_total(holding, price):
    return (holding * price)


def calc_change(price, open):
    return (price - open)


def enrichWithPriceData(item):
    ticker = item['ticker']
    price = prices.get_price(ticker)
    # if price = None:

    change = calc_change(price['price'], price['open'])
    item['change'] = change
    item['price'] = price['price']
    item['movement'] = calc_movement(change, price['price'])
    item['total_change'] = calc_total_change(item['qty'], change)
    item['total'] = calc_total(item['qty'], price['price'])

    # enrich with product data
    #  product = product.get(i['ticker'])
    item['name'] = 'Microsoft Ltd'
    item['ccy'] = "USD"
    item['symbol'] = "$"
    # enrich with spot is necessary
    # Might do once at ui level...?????
    # if portfolioCcy != accetCcy
    item['spot'] = 1.2922
    return item


def get_holding(userId, ticker):
    resval = balances.get_balance(userId, ticker)
    # f queryresult.count() == 0:
    #     return "No Results"
    if resval is None:
        return

    resval = enrichWithPriceData(resval)
    return resval


def get_holdings(userId):
    queryresult = balances.get_balances(userId)

    if queryresult.count() == 0:
        return "No Results"
    resval = []

    for item in queryresult:
        resval.append(enrichWithPriceData(item))
    return resval
