import logging
from api.products.repositories.products import get_product
from api.repositories.prices_repo import get_price_now, get_price_trend, get_price_latest

log = logging.getLogger(__name__)


def get_ticker(ticker: str) -> dict:
    try:
        product = get_product(ticker)
        print(product)
        price, isStale = lookup_price(ticker)
        print(price)
        trend_list = build_price_trend(ticker, 30)

        response = {
            "ccy": product["quote"]["currency"],
            "change": price["change"],
            "id": ticker,
            "movement": price["movement"],
            "name": product["name"],
            "price": price["price"],
            "spot": 1,
            "symbol": product["quote"]["symbol"],
            "ticker": ticker,
            "displayTicker": product["displayTicker"],
            "trend":  trend_list,
            "isStalePrice": isStale
        }
    except (KeyError) as error_key:
        log.error("KeyError found when building watchlist: %s" % error_key)
        return {}
    return response


def lookup_price(ticker: str) -> (dict, bool):
    isStale = False
    price = get_price_now(ticker)
    if price is None:
        price = get_price_latest(ticker)
        isStale = True
    return price, isStale


def build_price_trend(ticker: str, days: int) -> list:
    price_trend = list(get_price_trend(ticker, days))
    tList = []
    for x in price_trend:
        # I polluted the data with strings.  This is to filter them out.
        if type(x['price']) is float:
            tList.append(x['price'])
    return list(reversed(tList))
