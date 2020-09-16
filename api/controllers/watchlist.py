import logging
from api.repositories.products_repo import get_product
from api.repositories.prices_repo import get_price_now, get_price_trend, get_price_latest

log = logging.getLogger(__name__)


def get_ticker(ticker: str) -> dict:
    try:
        product = get_product(ticker)
        print(product)
        price, is_stale = lookup_price(ticker)
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
            "isStalePrice": is_stale
        }
    except (KeyError) as error_key:
        log.error("KeyError found when building watchlist: %s" % error_key)
        return {}
    return response


def lookup_price(ticker: str) -> (dict, bool):
    is_stale = False
    price = get_price_now(ticker)
    if price is None:
        price = get_price_latest(ticker)
        is_stale = True
    return price, is_stale


def build_price_trend(ticker: str, days: int) -> list:
    price_trend = list(get_price_trend(ticker, days))
    revered_price_list = []
    for x in price_trend:
        # I polluted the data with strings.  This is to filter them out.
        if type(x['price']) is float:
            revered_price_list.append(x['price'])
    return list(reversed(revered_price_list))
