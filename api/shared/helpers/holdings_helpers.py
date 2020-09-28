from api.shared.helpers.pricing_helper import calc_change, calc_movement, calc_total


def map_product(ticker: str, holding: dict, product: dict) -> dict:
    if product:
        holding['name'] = product['name']
        holding['ccy'] = product['quote']['currency']
        holding['symbol'] = product['quote']['symbol']
        holding['displayTicker'] = product['displayTicker']
    else:
        holding['name'] = ticker
        holding['ccy'] = 'USD'
        holding['symbol'] = '$'
        holding['displayTicker'] = ticker
    return holding


def map_spot(ticker: str, holding: dict, spot: dict) -> dict:
    if spot is None or 'price' not in spot:
        holding['spot'] = 1
    else:
        holding['spot'] = float(spot['price'])
    return holding


def map_price(holding: dict, price: dict) -> dict:
    asset_price = float(price['price'])
    asset_open = float(price['open'])
    asset_change = calc_change(asset_price, asset_open)

    if asset_price:
        holding['change'] = asset_change
        holding['price'] = asset_price
        holding['movement'] = calc_movement(asset_change, asset_price)
        holding['total_change'] = (holding['qty'] * asset_change / holding['spot'])
        holding['total'] = (calc_total(holding['qty'], asset_price) / holding['spot'])
    return holding
