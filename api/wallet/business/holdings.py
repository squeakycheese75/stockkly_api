
from api import auth
# from database.db import get_db

from api.wallet.repositories import balances
from api.products.repositories import prices, products
from api.profile.repository.users import get_user
# from stockklyApi.api.wallet.business import product

from bson import json_util
# from bson.objectid import ObjectId

# need some tests....:)
# Increase ÷ Original Number × 100.


def calc_movement(increase, price):
    if increase is None:
        return 0
    if price is None:
        return 0
    return (increase / price) * 100


def calc_total_change(holding, change):
    if holding is None:
        return 0
    if change is None:
        return 0
    return (holding * change)


def calc_total(holding, price):
    if holding is None:
        return 0
    if price is None:
        return 0
    return (holding * price)


def calc_change(price, open):
    if price is None:
        return 0
    if open is None:
        return 0
    return (price - open)


def enrichWithPriceData(item, userCcy):
    ticker = item['ticker']
    # enrich with product data
    product = products.get_product(ticker)
    if product:
        item['name'] = product['name']
        item['ccy'] = product['quote']['currency']
        item['symbol'] = product['quote']['symbol']
        item['displayTicker'] = product['displayTicker']
    else:
        item['name'] = 'na'
        item['ccy'] = 'na'
        item['symbol'] = 'na'
        item['displayTicker'] = ticker

    if item['ccy'] == userCcy:
        item['spot'] = 1
    else:
        spotTicker = userCcy + ":" + item['ccy']
        spot = prices.get_price_latest(spotTicker)
        item['spot'] = float(spot['price'])

    priceEntity = prices.get_price_now(ticker)
    if not priceEntity:
        priceEntity = prices.get_price_latest(ticker)

    price = priceEntity['price']
    open = priceEntity['open']

    if product['sector'] == 'Fund':
        previousPrice = prices.get_price_previous(ticker, priceEntity['priceDate'])
        open = previousPrice['price']

    if price:
        change = calc_change(price, open)
        item['change'] = change
        item['price'] = price
        item['movement'] = calc_movement(change, price)
        item['total_change'] = (calc_total_change(item['qty'], change) / item['spot'])
        item['total'] = (calc_total(item['qty'], price) / item['spot'])
    else:
        item['change'] = 0
        item['price'] = 0
        item['movement'] = 0
        item['total_change'] = 0
        item['total'] = 0

    return item


def get_holding(userId, ticker):
    resval = balances.get_balance(userId, ticker)
    # f queryresult.count() == 0:
    #     return "No Results"
    if resval is None:
        return

    userProfile = get_user(userId)

    resval = enrichWithPriceData(resval, userProfile['currency'])
    return resval


def get_holdings(userId):

    userProfile = get_user(userId)

    queryresult = balances.get_balances(userId)

    if queryresult.count() == 0:
        return "No Results"
    resval = []

    for item in queryresult:
        resval.append(enrichWithPriceData(item, userProfile['currency']))
        # print(resval)
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
