import pandas as pd
import json
from api.repositories import balances_repo, products_repo, prices_repo, users_repo, transactions_repo
from api.shared.helpers.pricing_helper import calc_change, calc_movement, calc_total, calc_total_change, calculate_asset_balance


def calculate_balance(user_id, ticker) -> dict:
    transactions = transactions_repo.get_transaction_history_for_user_and_product(user_id, ticker)
    return calculate_asset_balance(transactions, ticker, user_id)


def enrich_with_price_data(item: dict, user_ccy: str = 'GBP') -> dict:
    ticker = item['ticker']
    # enrich with product data
    product = products_repo.get_product(ticker)
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

    if item['ccy'] == user_ccy:
        item['spot'] = 1
    else:
        spot_ticker = user_ccy + ":" + item['ccy']
        spot = prices_repo.get_price_latest(spot_ticker)
        if spot is None:
            item['spot'] = 1
        else:
            item['spot'] = float(spot['price'])

    price_entity = prices_repo.get_price_now(ticker)
    if not price_entity:
        price_entity = prices_repo.get_price_latest(ticker)

    price = float(price_entity['price'])
    price_open = float(price_entity['open'])

    if product['sector'] == 'Fund':
        previous_price = prices_repo.get_price_previous(ticker, price_entity['priceDate'])
        price_open = previous_price['price']

    if price:
        change = calc_change(price, price_open)
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


def get_holding(user_id, ticker):
    resval = balances_repo.get_balance(user_id, ticker)
    if resval is None:
        return

    user_profile = users_repo.get_user(user_id)

    resval = enrich_with_price_data(resval, user_profile['currency'])
    return resval


def get_holdings(user_id):
    user_profile = users_repo.get_user(user_id)
    query_result = balances_repo.get_balances(user_id)
    if query_result.count() == 0:
        return "No Results"
    resval = []

    for item in query_result:
        quantity = item['qty']
        if quantity != 0:
            resval.append(enrich_with_price_data(item, user_profile['currency']))
    return resval


def get_holdings_historical(user_id):
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


def update_balance(user_id, ticker, qty):
    holding = get_holding(user_id, ticker)
    response = ''
    if holding is None:
        data = {
            'ticker': ticker,
            'userId': user_id,
            'qty': float(qty)
        }
        response = balances_repo.create_balance(user_id, data)
    else:
        new_balance = calculate_balance(user_id, ticker)
        response = balances_repo.update_balance(user_id, ticker, new_balance['qty'])
    return response
