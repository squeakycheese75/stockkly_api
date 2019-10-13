import pandas as pd
import json


from api.products.repositories.products import get_product
from api.products.repositories.prices import get_price_now, get_price_trend, get_price_latest


def get_historical(ticker, span):
    try:
        # lookup prices
        history = get_price_trend(ticker, span)
        # build a list
        l = []
        for x in history:
            if type(x['price']) is float:
                l.append(x)
        if not l:
            return None
        # convert to dataframe and format for the chart
        df = pd.DataFrame(l)
        df = df.set_index(pd.DatetimeIndex(df['priceDate']).strftime("%Y-%m-%d"))
        # drop the priceDate column
        target_column = 'priceDate'
        resval = df.drop(target_column, axis=1)
        # resval.head()
        response2 = resval.to_json(date_format='iso')
        rv = json.loads(response2)
        response = rv['price']
    except:
        response = None
    return response


def get_price(ticker):

    response = get_price_latest(ticker)

    product = get_product(ticker)
    if product:
        response['symbol'] = product['quote']['symbol']
        response['displayTicker'] = product['displayTicker']

    return response
