
from pytest import mark
from api.shared.helpers.pricing_helper import calc_movement, calc_change, calc_total


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

