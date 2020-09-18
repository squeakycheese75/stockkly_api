
from pytest import mark
from api.shared.helpers.pricing_helper import calc_movement, calc_change, calc_total, calc_total_change, convert_price_list,calculate_asset_balance


@mark.parametrize(
 "increase, price, expected_result",
 [(0, 0, 0),
  (0, 1, 0),
  (1, 0, 0),
  (None, 0, 0),
  (0, None, 0),
  (None, None, 0),
  (0.20, 2.00, 10.0),
  (-0.20, 2.00, -10.0),
  ]
)
def test_we_correctly_calculate_price_movement(increase, price, expected_result):
    resval = calc_movement(increase, price)
    assert resval == expected_result


@mark.parametrize(
 "price, open, expected_result",
 [(0, 0, 0),
  (0, 1, -1),
  (None, 0, 0),
  (0, None, 0),
  (None, None, 0),
  (0.20, 2.00, -1.8),
  (-0.20, 2.00, -2.2),
  ]
)
def test_we_correctly_calc_change(price, open, expected_result):
    resval = calc_change(price, open)
    assert resval == expected_result


@mark.parametrize(
 "holding, price, expected_result",
 [(0, 0, 0),
  (0, 1, 0),
  (None, 0, 0),
  (0, None, 0),
  (None, None, 0),
  (100, 2.10, 210),
  (10, -2.00, -20),
  ]
)
def test_calc_total(holding, price, expected_result):
    resval = calc_total(holding, price)
    assert resval == expected_result

@mark.parametrize(
 "holding, change, expected_result",
 [(0, 0, 0),
  (0, 1, 0),
  (None, 0, 0),
  (0, None, 0),
  (None, None, 0),
  (100, 2.10, 210),
  (10, -2.00, -20),
  ]
)
def test_calc_total_change(holding, change, expected_result):
    resval = calc_total_change(holding, change)
    assert resval == expected_result

def test_the_convert_price_list_flattens_a_datasource():
  prices = [
    {"price": 1.99, "priceDate": '2020-01-31', "ticker": "GOLD:OZ:GBP",},
    {"price": 1.98, "priceDate": '2020-01-30', "ticker": "GOLD:OZ:GBP",},
    {"price": 1.97, "priceDate": '2020-01-29', "ticker": "GOLD:OZ:GBP",},
  ]
  resval = convert_price_list(prices)
  assert resval == {'2020-01-31': 1.99, '2020-01-30': 1.98, '2020-01-29': 1.97}


def test_calculate_asset_balance():
  transactions = [
    {'transtype': 'BUY', 'quantity': 100},
    {'transtype': 'Sell', 'quantity': 10}
    ]
  resval = calculate_asset_balance(transactions, 'BTC:USD', 'test@user')
  assert resval.get('qty') == 90


@mark.parametrize(
 "transactions,  expected_balance",
 [([
    {'transtype': 'BUY', 'quantity': 100},
    {'transtype': 'Sell', 'quantity': 10}
  ], 90),
  ([
    {'transtype': 'BUY', 'quantity': 100},
    {'transtype': 'BUY', 'quantity': 10}
  ], 110),
  ]
)
def test_calculate_asset_balance2(transactions, expected_balance):
  resval = calculate_asset_balance(transactions, 'BTC:USD', 'test@user')
  assert resval.get('qty') == expected_balance