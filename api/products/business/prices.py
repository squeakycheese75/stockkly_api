import pandas as pd

from api.products.repositories.products import get_product
from api.products.repositories.prices import get_price_now, get_price_trend


def get_historical(ticker, span):
    try:
        # lookup prices
        history = get_price_trend(ticker, span)
        # build a list
        l = []
        for x in history:
            l.append(x)
        # convert to dataframe and format for the chart
        df = pd.DataFrame(l)
        df = df.set_index(pd.DatetimeIndex(df['priceDate']).strftime("%Y-%m-%d"))
        # drop the priceDate column
        target_column = 'priceDate'
        resval = df.drop(target_column, axis=1)
        # resval.head()
        response = resval.to_json(date_format='iso')
    except:
        response = None
    return response
