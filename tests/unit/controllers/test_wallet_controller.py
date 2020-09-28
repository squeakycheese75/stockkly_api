from unittest.mock import patch
from api.controllers.wallet import calculate_balance, enrich_with_price_data, get_holding, update_balance

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


@patch("api.controllers.wallet.balances_repo.create_balance")
@patch("api.controllers.wallet.get_holding")
def test_update_balance_creates_a_new_balace(mock_get_holding, mock_create_balance):
    test_ticker = 'BTC:USD'
    test_qty = 100
    test_user = 'user'

    mock_get_holding.return_value = None
    mock_create_balance.return_value = {}
    
    data = {
            'ticker': test_ticker,
            'userId': test_user,
            'qty': float(test_qty)
        }

    resval = update_balance(test_user, test_ticker, test_qty)
    
    mock_create_balance.assert_called_once_with(test_user, data)
    assert resval == {}


@patch("api.controllers.wallet.calculate_balance")
@patch("api.controllers.wallet.balances_repo.update_balance")
@patch("api.controllers.wallet.get_holding")
def test_update_balance_creates_a_new_balace2(mock_get_holding, mock_update_balance, mock_calculate_balance):
    test_ticker = 'BTC:USD'
    test_qty = 100
    test_user = 'user'
    test_holding = {
      'ticker': 'BTC:USD',
      'qty': 10
    }
    test_balance = {
      'qty': 90,
      'ticker': test_ticker,
      'userId': test_user
    }

    mock_get_holding.return_value = test_holding
    mock_update_balance.return_value = {}
    calculate_balance.return_value = test_balance

    resval = update_balance(test_user, test_ticker, test_qty)
    
    mock_update_balance.assert_called_once()
    assert resval == {}

