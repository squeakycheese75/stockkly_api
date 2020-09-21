from pytest import mark
from api.shared.helpers.holdings_helpers import map_product, map_spot, map_price


def test_map_product_if_data_present():
    test_ticker = 'BTC:USD'
    test_holding = {
      'ticker': test_ticker
    }

    test_product = {
      'ticker': test_ticker, 
      'name': 'Bitcoin',
      'quote': {
        'currency': 'USD',
        'symbol': '$'
      },
      'displayTicker': test_ticker
    }
    resval = map_product(test_ticker, test_holding, test_product)
    assert resval['ticker'] == 'BTC:USD'
    assert resval['name'] == 'Bitcoin'
    assert resval['symbol'] == '$'
    assert resval['ccy'] == 'USD'
    assert resval['displayTicker'] == 'BTC:USD'

def test_map_product_if_data_not_present():
    test_ticker = 'BTC:USD'
    test_holding = {
      'ticker': test_ticker
    }

    resval = map_product(test_ticker, test_holding, None)
    assert resval['ticker'] == 'BTC:USD'
    assert resval['name'] == 'BTC:USD'
    assert resval['symbol'] == '$'
    assert resval['ccy'] == 'USD'
    assert resval['displayTicker'] == 'BTC:USD'


@mark.parametrize(
 "spot, expected_result",
 [({}, 1),
  (None, 1),
  ({'price': 1.99}, 1.99)
  ]
)
def test_map_spot_handles_inputs(spot, expected_result):
    test_ticker = 'BTC:USD'
    test_holding = {
      'ticker': test_ticker
    }

    resval = map_spot(test_ticker, test_holding, spot)
    assert resval['ticker'] == 'BTC:USD'
    assert resval['spot'] == expected_result


def test_map_price():
    test_ticker = 'BTC:USD'
    test_holding = {
      'ticker': test_ticker,
      'qty': 100,
      'spot': 1.3
    }
    test_price = {
      'price': 10.99,
      'open': 10.67
    }
    resval = map_price(test_holding, test_price)
    assert round(resval['change'], 2) == 0.32
    assert resval['price'] == 10.99
    assert round(resval['movement'], 2) == 2.91
    assert round(resval['total_change'], 2)== 24.62
    assert round(resval['total'], 2) == 845.38
