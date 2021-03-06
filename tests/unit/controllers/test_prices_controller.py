from api.controllers.prices import get_price, get_historical, clean_price_list
from unittest.mock import patch
import json


@patch("api.controllers.prices.get_product")
@patch("api.controllers.prices.get_price_latest")
def test_we_return_a_price(mock_get_price_latest, mock_get_product):
  dummy_price = {
    'price': 12.34,
    'symbol': 'BTC:USD',
  }

  dummy_product = {
    'quote': {
      'symbol': 'BTC:USD'
    },
    'displayTicker':'BTC'
  }

  mock_get_price_latest.return_value = dummy_price
  mock_get_product.return_value = dummy_product

  resval = get_price('BTC:USD')
  assert resval.get('price') == 12.34
  assert resval.get('displayTicker') == 'BTC'


@patch("api.controllers.prices.get_product")
@patch("api.controllers.prices.get_price_latest")
def test_somethi(get_price_latest, mock_get_product):
  dummy_price = {
    'price': 12.34,
    'symbol': 'BTC:USD',
  }
  get_price_latest.return_value = dummy_price
  mock_get_product.return_value = None

  resval = get_price('BTC:USD')
  assert resval.get('price') == 12.34
  assert resval.get('displayTicker') == None


@patch("api.controllers.prices.get_price_trend")
def test_clean_price_list_returns_empty_list_if_no_history(mock_get_price_trend):
  mock_get_price_trend.return_value == {}
  resval = clean_price_list('BTC:USD', 100)
  assert resval == []


@patch("api.controllers.prices.clean_price_list")
def test_we_return_empty_list_if_no_prices(mock_clean_price_list):
  mock_clean_price_list.return_value = []
  resval = get_historical('GOLD:OZ:GBP', 3)
  assert resval == []


@patch("api.controllers.prices.get_price_trend")
def test_we_return_a_full_list_of_cleaned_prices_for_get_historical(get_price_trend):
  p1 = [
    {"price": 1.99, "priceDate": '2020-01-31', "ticker": "GOLD:OZ:GBP",},
    {"price": 1.98, "priceDate": '2020-01-30', "ticker": "GOLD:OZ:GBP",},
    {"price": 1.97, "priceDate": '2020-01-29', "ticker": "GOLD:OZ:GBP",},
  ]

  get_price_trend.return_value = p1
  resval = get_historical('GOLD:OZ:GBP', 3)
  assert resval == {'2020-01-31': 1.99, '2020-01-30': 1.98, '2020-01-29': 1.97}
  assert type(resval) == dict



