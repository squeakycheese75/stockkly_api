from api.shared.helpers.pricing_helper import calc_change, calc_movement, calc_total


def build_holding(holding: dict,
                  product: dict,
                  price: dict,
                  spot: dict = {'price': 1},
                  user_ccy: str = 'GBP') -> dict:
    ticker = holding['ticker']
    # enrich with product data
    if product:
        holding['name'] = product['name']
        holding['ccy'] = product['quote']['currency']
        holding['symbol'] = product['quote']['symbol']
        holding['displayTicker'] = product['displayTicker']
    else:
        holding['name'] = 'na'
        holding['ccy'] = 'na'
        holding['symbol'] = 'na'
        holding['displayTicker'] = ticker
    # enrich with spot
    holding['spot'] == float(spot['price'])

    # enrich with price
    asset_price = float(price['price'])
    asset_open = float(price['open'])

    if asset_price:
        change = calc_change(price, asset_open)
        holding['change'] = change
        holding['price'] = price
        holding['movement'] = calc_movement(change, price)
        holding['total_change'] = (calc_movement(holding['qty'], change) / holding['spot'])
        holding['total'] = (calc_total(holding['qty'], price) / holding['spot'])
    return holding
