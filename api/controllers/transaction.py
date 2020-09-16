from api.repositories import transactions_repo
from api.controllers.holdings import update_balance


def create_transaction(data, userId):
    response = transactions_repo.create_transaction(data, userId)

    update_balance(userId, data['ticker'], data['quantity'])
    return response


def upsert_transaction(data, userId):
    tran = transactions_repo.get_transaction_by_id(data['id'])
    response = transactions_repo.upsert_transaction(data, userId)

    quantity = (float(data['quantity']) - float(tran['quantity']))

    update_balance(userId, data['ticker'], quantity)
    return response


def delete_transaction(userId, transactionId):
    tran = transactions_repo.get_transaction_by_id(transactionId)

    quantity = (float(tran['quantity']) * -1)
    update_balance(userId, tran['ticker'], quantity)

    response = transactions_repo.delete_transaction(transactionId)
    return response
