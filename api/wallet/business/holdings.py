
from api import auth
from database.db import get_db

from api.wallet.repositories import balances
from api.products.repositories import products, prices
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
    if price:
        change = calc_change(price['price'], price['open'])
        item['change'] = change
        item['price'] = price['price']
        item['movement'] = calc_movement(change, price['price'])
        item['total_change'] = calc_total_change(item['qty'], change)
        item['total'] = calc_total(item['qty'], price['price'])

    # enrich with product data
    product = products.get_product(ticker)
    if product:
        item['name'] = product['name']
        item['ccy'] = product['quote']['currency']
        item['symbol'] = product['quote']['symbol']
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
        print(resval)
    return resval


def update_balance(userId, ticker, qty):
    holding = get_holding(userId, ticker)
    response = ''
    if holding == None:
        data = {
            'ticker': ticker,
            'userId': userId,
            'qty': qty
        }
        response = balances.create_balance(userId, data)
    else:
        old_qty = holding['qty']
        new_qty = old_qty + qty
        response = balances.update_balance(userId, ticker, new_qty)
    return response
