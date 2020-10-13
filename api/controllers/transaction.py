#!/usr/bin/env python
"""The transactions controller"""

from api.repositories import transactions_repo
from api.controllers.wallet import update_balance


def create_transaction(data, user_id):
    response = transactions_repo.create_transaction(data, user_id)

    update_balance(user_id, data['ticker'], data['quantity'])
    return response


def upsert_transaction(data, user_id):
    tran = transactions_repo.get_transaction_by_id(data['id'])
    response = transactions_repo.upsert_transaction(data, user_id)

    quantity = (float(data['quantity']) - float(tran['quantity']))
    update_balance(user_id, data['ticker'], quantity)
    return response


def delete_transaction(user_id, transaction_id):
    tran = transactions_repo.get_transaction_by_id(transaction_id)

    quantity = (float(tran['quantity']) * -1)
    update_balance(user_id, tran['ticker'], quantity)

    response = transactions_repo.delete_transaction(transaction_id)
    return response
