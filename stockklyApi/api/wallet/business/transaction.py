# todo

# insert transaction
# need to udate the live holding

from stockklyApi.api.wallet.repositories import transactions as transactionRepo
from stockklyApi.api.wallet.business.holdings import update_balance


def create_transaction(data, userId):
    # transactionRepo.create_transaction(data)
    response = transactionRepo.create_transaction(data, userId)

    update_balance(userId, data['ticker'], data['quantity'])
    return response


def upsert_transaction(data, userId):
    response = transactionRepo.upsert_transaction(data, userId)

    update_balance(userId, data['ticker'], data['quantity'])
    return response
