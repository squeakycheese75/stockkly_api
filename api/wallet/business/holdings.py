import pandas as pd
import json
from api import auth
from api.wallet.repositories import balances
from api.products.repositories import products
from api.repositories import prices_repo
from api.profile.repository.users import get_user
from api.wallet.repositories.transactions import get_transaction_history_for_user_and_product
from bson import json_util


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


def calculate_balance(userId, ticker):
    transactions = get_transaction_history_for_user_and_product(userId, ticker)
    balance = {
        'ticker': ticker,
        'userId': userId,
        'qty': 0
    }
    for item in transactions:
        if item['transtype'].upper() == "BUY":
            balance['qty'] += float(item['quantity'])
        else:
            balance['qty'] -= float(item['quantity'])
    return balance


def enrichWithPriceData(item, userCcy):
    ticker = item['ticker']
    # print(ticker)
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
        spot = prices_repo.get_price_latest(spotTicker)
        if spot is None:
            item['spot'] = 1
        else:
            item['spot'] = float(spot['price'])

    priceEntity = prices_repo.get_price_now(ticker)
    if not priceEntity:
        priceEntity = prices_repo.get_price_latest(ticker)

    price = float(priceEntity['price'])
    open = float(priceEntity['open'])

    if product['sector'] == 'Fund':
        previousPrice = prices_repo.get_price_previous(ticker, priceEntity['priceDate'])
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
        quantity = item['qty']
        if quantity != 0:
            resval.append(enrichWithPriceData(item, userProfile['currency']))
    return resval


def get_holdings_historical(userId):
    df = pd.DataFrame(columns=["balance", "balanceDate"], data=[
        [10000.00, '2019-11-01'],
        [9000.00, '2019-10-01'],
        [11000.99, '2019-09-01'],
        [8666.99, '2019-08-01'],
        [7999.99, '2019-07-01'],
        [8200.00, '2019-06-01'],
        [9000.00, '2019-05-01'],
        [10600.99, '2019-04-01'],
        [8666.99, '2019-03-01'],
        [7999.99, '2019-02-01'],
        [9779.99, '2019-01-01']
    ])
    df = df.set_index(pd.DatetimeIndex(df['balanceDate']).strftime("%Y-%m-%d"))
    resval = df.drop('balanceDate', axis=1)
    response = resval.to_json(date_format='iso')
    rv = json.loads(response)
    response2 = rv['balance']
    return response2


def update_balance(userId, ticker, qty):
    holding = get_holding(userId, ticker)
    response = ''
    if holding == None:
        data = {
            'ticker': ticker,
            'userId': userId,
            'qty': float(qty)
        }
        response = balances.create_balance(userId, data)
    else:
        # old_qty = float(holding['qty'])
        # new_qty = old_qty + float(qty)
        # response = balances.update_balance(userId, ticker, new_qty)
        new_balance = calculate_balance(userId, ticker)
        response = balances.update_balance(userId, ticker, new_balance['qty'])
    return response


# def get_historical_holdings():
    # userProfile = get_user(userId)

    # queryresult = balances.get_balances(userId)

    # if queryresult.count() == 0:
    #     return "No Results"
    # resval = []

    # for item in queryresult:
    #     quantity = item['qty']
    #     if quantity != 0:
    #         resval.append(enrichWithPriceData(item, userProfile['currency']))
    # return resval
