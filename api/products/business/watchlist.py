from api.products.repositories.products import get_product
from api.products.repositories.prices import get_price_now


def get_ticker(ticker):
    try:
        # lookup product
        product = get_product(ticker)
        # lookup price
        price = get_price_now(ticker)
        response = {
            "ccy": product["quote"]["currency"],
            "change": price["change"],
            "id": ticker,
            "movement": price["movement"],
            "name": product["name"],
            "price": price["price"],
            "spot": 0,
            "symbol": product["quote"]["symbol"],
            "ticker": ticker
        }
    except:
        response = None
    return response
