from unittest.mock import patch
from api.controllers.wallet import calculate_balance, enrich_with_price_data, get_holding

@patch("api.controllers.wallet.transactions_repo.get_transaction_history_for_user_and_product")
def test_calculate_balance(mock_transactions):
    test_ticker = 'BTC:USD'
    test_user = 'dummyUser'
    mock_transactions.return_value = [
      {'transtype': 'BUY', 'quantity': 100},
      {'transtype': 'Sell', 'quantity': 10}
    ]
    resval = calculate_balance('dummyUser', 'BTC:USD')
    assert resval.get('qty') == 90
    assert resval.get('ticker') == test_ticker
    assert resval.get('userId') == test_user


@patch("api.controllers.wallet.prices_repo.get_price_latest")
@patch("api.controllers.wallet.prices_repo.get_price_now")
@patch("api.controllers.wallet.products_repo.get_product")
def test_enrich_holdings(mock_get_product, mock_get_price_now, mock_get_price_latest):
  test_ticker = 'BTC:USD'
  test_holding = {
    'ticker': 'BTC:USD',
    'qty': 9.33
  }
  test_user_currency = 'GBP'
  test_product = {
      'ticker': test_ticker, 
      'name': 'Bitcoin',
      'quote': {
        'currency': 'USD',
        'symbol': '$'
      },
      'displayTicker': test_ticker,
      'sector': 'Crypto'
    }
  test_price = {
      'price': 10966.74,
      'open': 10944.98
    }
  test_spot = {'price': 1.29}
  mock_get_price_now.return_value = test_price
  mock_get_product.return_value  = test_product
  mock_get_price_latest.return_value = test_spot
  resval = enrich_with_price_data(test_holding, test_user_currency)
  assert resval['name']  == 'Bitcoin'
  assert round(resval['total_change'], 2)  == 157.38
  assert round(resval['total'], 2) == 79317.58


@patch("api.controllers.wallet.prices_repo.get_price_latest")
@patch("api.controllers.wallet.prices_repo.get_price_now")
@patch("api.controllers.wallet.products_repo.get_product")
def test_enrich_holdings_new(mock_get_product, mock_get_price_now, mock_get_price_latest):
  test_ticker = 'BTC:USD'
  test_holding = {
    'ticker': 'BTC:USD',
    'qty': 9.33
  }
  test_user_currency = 'USD'
  test_product = {
      'ticker': test_ticker, 
      'name': 'Bitcoin',
      'quote': {
        'currency': 'USD',
        'symbol': '$'
      },
      'displayTicker': test_ticker,
      'sector': 'Crypto'
    }
  test_price = {
      'price': 10966.74,
      'open': 10944.98
    }
  test_spot = {'price': 1.29}
  mock_get_price_now.return_value = test_price
  mock_get_product.return_value  = test_product
  mock_get_price_latest.return_value = test_spot
  resval = enrich_with_price_data(test_holding, test_user_currency)
  assert resval['name']  == 'Bitcoin'
  assert round(resval['total_change'], 2)  == 203.02
  assert round(resval['total'], 2) == 102319.68


@patch("api.controllers.wallet.balances_repo.get_balance")
@patch("api.controllers.wallet.users_repo.get_user")
def test_get_holding_return_empty_if_no_balance(mock_get_user, mock_get_balance):
    test_ticker = 'BTC:USD'
    test_user = 'dummyUser'

    mock_get_balance.return_value = None
    mock_get_user = {}
    resval = get_holding(test_user, test_ticker)
    assert resval == None


@patch("api.controllers.wallet.balances_repo.get_balance")
@patch("api.controllers.wallet.users_repo.get_user")
@patch("api.controllers.wallet.enrich_with_price_data")
def test_get_holding(mock_enrich_with_price_data, mock_get_user, mock_get_balance):
    test_ticker = 'BTC:USD'
    test_user = {'currency': 'GBP'}
    dummy_result  = {'ticker': test_ticker}

    mock_get_user.return_value = test_user
    mock_get_balance.return_value = dummy_result
    mock_enrich_with_price_data.return_value = dummy_result

    resval = get_holding(test_user, test_ticker)
    mock_enrich_with_price_data.assert_called_once()
    mock_get_balance.assert_called_once()
    mock_get_user.assert_called_once()
    assert resval == dummy_result
