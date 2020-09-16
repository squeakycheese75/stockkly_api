from api.business.watchlist import get_ticker, lookup_price, build_price_trend, get_ticker
from unittest.mock import patch
import json


@patch("api.business.watchlist.get_price_now")
def test_the_lookup_price_identifies_as_notStale_if_price_exists(mock_get_price_now):
    dummy_price = {
      'price': 12.34,
      'symbol': 'BTC:USD',
    }
    mock_get_price_now.return_value = dummy_price

    price, isStyle = lookup_price('GOLD:OZ:GBP')
    assert price == dummy_price
    assert not isStyle


@patch("api.business.watchlist.get_price_now")
@patch("api.business.watchlist.get_price_latest")
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


@patch("api.business.watchlist.get_price_trend")
def test_build_price_trend(mock_get_price_trend):
    mock_get_price_trend.return_value = []
    resval = build_price_trend('GOLD:OZ:GBP', 30)
    assert resval == []


@patch("api.business.watchlist.get_price_trend")
def test_build_price_trend_reverses_list(mock_get_price_trend):
    dummy_prices = [
        {'price': 1.11, 'priceDate': '2020-01-01'},
        {'price': 1.12, 'priceDate': '2020-01-02'},
        {'price': 1.13, 'priceDate': '2020-01-02'},
      ]
    mock_get_price_trend.return_value = dummy_prices
    resval = build_price_trend('GOLD:OZ:GBP', 30)
    assert resval == [1.13, 1.12, 1.11]


@patch("api.business.watchlist.get_product")
@patch("api.business.watchlist.lookup_price")
@patch("api.business.watchlist.build_price_trend")
def test_get_ticker(mock_build_price_trend, mock_lookup_price, mock_get_product):
    dummy_product = {
      'quote': {
        'symbol': 'BTC:USD'
      },
      'displayTicker':'BTC'
    }
    dummy_price = {
    'price': 12.34,
    'symbol': 'BTC:USD',
    }

    mock_get_product.return_value = dummy_product
    mock_lookup_price.return_value = dummy_price, False
    mock_build_price_trend.return_value = []

    resval = get_ticker('GOLD:OZ:GBP')
    assert resval == {}


@patch("api.business.watchlist.get_product")
@patch("api.business.watchlist.lookup_price")
@patch("api.business.watchlist.build_price_trend")
def test_get_ticker2(mock_build_price_trend, mock_lookup_price, mock_get_product):
    dummy_product = {
      'quote': {
        'symbol': 'BTC:USD',
        'currency': 'USD'
      },
      'displayTicker':'BTC',
      'name': 'Bitcoin'
    }
    dummy_price = {
      'price': 12.34,
      'symbol': 'BTC:USD',
      'change': 0.01,
      'movement': 0.1
    }

    mock_get_product.return_value = dummy_product
    mock_lookup_price.return_value = dummy_price, False
    mock_build_price_trend.return_value = []

    resval = get_ticker('GOLD:OZ:GBP')
    assert resval.get('name')  == 'Bitcoin'
    assert resval.get('price')  == 12.34