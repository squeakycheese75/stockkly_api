from unittest.mock import patch
from api.controllers.holdings import calculate_balance, enrich_with_price_data

@patch("api.controllers.holdings.transactions_repo.get_transaction_history_for_user_and_product")
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


# @patch("api.controllers.holdings.get_holding")
# def test_update_balance(mock_get_holding):
#     mock_get_holding.return_value == ''

# def test_enrich_with_price_data():
#   asset_balance = {
#     'ticker':'BTC:USD'
#   }
#   resval = enrich_with_price_data(asset_balance, 'GBP')
