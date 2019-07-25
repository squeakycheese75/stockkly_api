from api.products.repositories.products import get_product
from api.products.repositories.prices import get_price_now, get_price_trend


def get_ticker(ticker):
    try:
        # lookup product
        product = get_product(ticker)
        # lookup price
        price = get_price_now(ticker)
        trend = list(get_price_trend(ticker, 30))
        tList = []
        for x in trend:
            # tList.append(x['price'])
            # I polluted the data with strings.  This is to filter them out.
            if type(x['price']) is float:
                tList.append(x['price'])
        response = {
            "ccy": product["quote"]["currency"],
            "change": price["change"],
            "id": ticker,
            "movement": price["movement"],
            "name": product["name"],
            "price": price["price"],
            "spot": 0,
            "symbol": product["quote"]["symbol"],
            "ticker": ticker,
            "displayTicker": product["displayTicker"],
            "trend":  tList
        }
    except:
        response = None
    return response
