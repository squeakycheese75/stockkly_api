import pandas as pd
from json import loads
from api.products.repositories.products import get_product
from api.products.repositories.prices import get_price_now, get_price_trend, get_price_latest


def get_historical(ticker, span):
    try:
        
        l = clean_price_list(ticker, span)
        if not l:
            return None

        # convert to dataframe and format for the chart
        df = pd.DataFrame(l)
        df = df.set_index(pd.DatetimeIndex(df['priceDate']).strftime("%Y-%m-%d"))
        # drop the priceDate column
        target_column = 'priceDate'
        resval = df.drop(target_column, axis=1)
        response2 = resval.to_json(date_format='iso')
        rv = loads(response2)
        response = rv['price']
    except (KeyError, TypeError, ValueError, AttributeError) as error_ee:
        print(error_ee)
    return response


def get_price(ticker) -> dict:
    response = get_price_latest(ticker)
    product = get_product(ticker)
    if product:
        response['symbol'] = product['quote']['symbol']
        response['displayTicker'] = product['displayTicker']
    return response


def clean_price_list(ticker: str, span: int) -> list:
    price_history = get_price_trend(ticker, span)
    price_list = []
    for p in price_history:
        if type(p['price']) is float:
            price_list.append(p)
    return price_list
