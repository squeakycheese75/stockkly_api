from api.wallet.repositories import transactions as transactionRepo
from api.wallet.business.holdings import update_balance, get_holding


def create_transaction(data, userId):
    response = transactionRepo.create_transaction(data, userId)

    update_balance(userId, data['ticker'], data['quantity'])
    return response


def upsert_transaction(data, userId):
    tran = transactionRepo.get_transaction_by_id(data['id'])
    response = transactionRepo.upsert_transaction(data, userId)

    quantity = (float(data['quantity']) - float(tran['quantity']))

    update_balance(userId, data['ticker'], quantity)
    return response


def delete_transaction(userId, transactionId):
    # need to update balances
    tran = transactionRepo.get_transaction_by_id(transactionId)

    quantity = (float(tran['quantity']) * -1)
    update_balance(userId, tran['ticker'], quantity)

    response = transactionRepo.delete_transaction(transactionId)
    return response
