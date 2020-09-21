import pandas as pd
from json import loads


def calc_movement(increase: float, price: float) -> float:
    if increase is None or price is None or price == 0:
        return 0
    return (increase / price) * 100


def calc_total_change(holding: float, change: float) -> float:
    if holding is None or change is None:
        return 0
    return (holding * change)


def calc_total(holding: float, price: float) -> float:
    if holding is None or price is None:
        return 0
    return (holding * price)


def calc_change(price: float, open: float) -> float:
    if price is None or open is None:
        return 0
    return (price - open)


def convert_price_list(price_list: list) -> dict:
    # convert to dataframe and format for the chart
    df = pd.DataFrame(price_list)
    df = df.set_index(pd.DatetimeIndex(df['priceDate']).strftime("%Y-%m-%d"))
    # drop the priceDate column
    target_column = 'priceDate'
    resval = df.drop(target_column, axis=1)

    r = resval.to_json(date_format='iso')
    rv = loads(r)
    return rv['price']


def calculate_asset_balance(transactions: list, ticker: str, user_id: str):
    balance = {
        'ticker': ticker,
        'userId': user_id,
        'qty': 0
    }
    for item in transactions:
        if item['transtype'].upper() == "BUY":
            balance['qty'] += float(item['quantity'])
        else:
            balance['qty'] -= float(item['quantity'])
    return balance
