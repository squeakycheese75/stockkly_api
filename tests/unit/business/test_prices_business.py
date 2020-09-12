from api.products.business.prices import get_price, get_historical, clean_price_list
from unittest.mock import patch

@patch("api.products.business.prices.get_product")
@patch("api.products.business.prices.get_price_latest")
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


@patch("api.products.business.prices.get_product")
@patch("api.products.business.prices.get_price_latest")
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


@patch("api.products.business.prices.get_price_trend")
def test_clean_price_list_returns_empty_list_if_no_history(mock_get_price_trend):
  mock_get_price_trend.return_value == {}
  resval = clean_price_list('BTC:USD', 100)
  assert resval == []