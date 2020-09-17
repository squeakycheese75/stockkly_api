from api.controllers.transaction import create_transaction, upsert_transaction, delete_transaction
from unittest.mock import patch

@patch("api.controllers.transaction.transactions_repo.create_transaction")
@patch("api.controllers.transaction.update_balance")
def test_create_transaction(mock_update_balance, mock_create_transaction):
    test_data = {  
      'ticker': 'BTC:USD',
      'quantity': 1234
      }
    test_user_id = '123456'
    test_response = 'test_response'

    mock_update_balance.return_value = test_response
    mock_create_transaction.return_value = test_response

    create_transaction(test_data, test_user_id)
    mock_create_transaction.assert_called_once_with(test_data, test_user_id)
    mock_update_balance.assert_called_once_with(test_user_id, test_data.get('ticker'), test_data.get('quantity'))


@patch("api.controllers.transaction.transactions_repo.get_transaction_by_id")
@patch("api.controllers.transaction.transactions_repo.upsert_transaction")
@patch("api.controllers.transaction.update_balance")
def test_upsert_transaction(mock_update_balance, mock_upsert_transaction, mock_get_transaction_by_id):
    test_data = {  
      'ticker': 'BTC:USD',
      'quantity': 100.0,
      'id': 1234
      }
    test_user_id = '123456'
    test_response = 'test_response'
    test_trans = {
      'quantity': 10.0
    }

    mock_update_balance.return_value = test_trans
    mock_upsert_transaction.return_value = test_response
    mock_get_transaction_by_id.return_value = test_trans
    
    upsert_transaction(test_data, test_user_id)
    mock_update_balance.assert_called_once_with(test_user_id, test_data.get('ticker'), 90)
    mock_upsert_transaction.assert_called_once_with(test_data, test_user_id)
    mock_get_transaction_by_id.assert_called_once_with(test_data.get('id'))


@patch("api.controllers.transaction.transactions_repo.get_transaction_by_id")
@patch("api.controllers.transaction.transactions_repo.delete_transaction")
@patch("api.controllers.transaction.update_balance")
def test_delete_transaction(mock_update_balance, mock_delete_transaction, mock_get_transaction_by_id):
    test_transaction_id = 1234
    test_user_id = '123456'
    test_response = 'test_response'
    test_trans = {
      'quantity': 10.0,
      'ticker': 'BTC:USD'
    }

    mock_update_balance.return_value = test_trans
    mock_delete_transaction.return_value = test_response
    mock_get_transaction_by_id.return_value = test_trans
    
    delete_transaction(test_user_id, test_transaction_id)
    mock_get_transaction_by_id.assert_called_once_with(test_transaction_id)
    mock_update_balance.assert_called_once_with(test_user_id, test_trans.get('ticker'), -10.0)
    mock_delete_transaction.assert_called_once_with(test_transaction_id)
