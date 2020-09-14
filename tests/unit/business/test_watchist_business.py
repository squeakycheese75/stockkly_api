from api.products.business.watchlist import get_ticker, lookup_price
from unittest.mock import patch
import json


@patch("api.products.business.watchlist.get_price_now")
def test_the_lookup_price_identifies_as_notStale_if_price_exists(mock_get_price_now):
  dummy_price = {
    'price': 12.34,
    'symbol': 'BTC:USD',
  }
  mock_get_price_now.return_value = dummy_price

  price, isStyle = lookup_price('GOLD:OZ:GBP')
  assert price == dummy_price
  assert not isStyle


@patch("api.products.business.watchlist.get_price_now")
@patch("api.products.business.watchlist.get_price_latest")
def test_the_lookup_price_identifies_as_stale(mock_get_price_now, mock_get_price_latest):
  dummy_price = {
    'price': 12.34,
    'symbol': 'BTC:USD',
  }
  mock_get_price_now.return_value = dummy_price
  mock_get_price_latest.return_value = None

  price, isStyle = lookup_price('GOLD:OZ:GBP')
  assert price == dummy_price
  assert isStyle