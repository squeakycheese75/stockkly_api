import logging
import json
from flask_restplus import Resource
from flask import request
from api import auth
from api.repositories.transactions_repo import get_transaction_history_for_user_and_product, get_transaction_history_for_user
from api.shared.serialisers import transaction
from api.controllers.transaction import upsert_transaction, create_transaction, delete_transaction
from api.cache import cache
from api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace('transactions', description='Operations related to wallet Transactions')

CACHE_PREFIX = 'auth:'


@ns.route('/')
class TransactionCollection(Resource):
    @auth.requires_auth
    @api.marshal_list_with(transaction)
    def get(self):
        """
        Returns list of all transactions for an authenticated user.
        """
        cache_key = CACHE_PREFIX + request.headers.get("Authorization", None)
        rv = cache.get(cache_key)
        if rv is None:
            user_info = auth.get_userinfo_with_token()
            rv = user_info['email']
            cache.set(cache_key, rv, timeout=60 * 50)

        cursor = get_transaction_history_for_user(rv)
        res = []
        for document in json.loads(cursor):
            doc = str(document["_id"]['$oid'])
            document['id'] = doc
            res.append(document)
        return res, 200

    @api.response(201, 'Transaction successfully created.')
    @api.expect(transaction)
    def post(self):
        user_info = auth.get_userinfo_with_token()
        user_email = user_info['email']
        data = request.json
        create_transaction(data, user_email)
        return None, 201


@ns.route('/<string:id>')
@api.response(404, 'Transaction not found.')
class TransactionItem(Resource):
    @auth.requires_auth
    @api.marshal_list_with(transaction)
    def get(self, id):
        """
        Returns list of products transactions for an authenticated user.
        """
        cache_key = CACHE_PREFIX + request.headers.get("Authorization", None)
        rv = cache.get(cache_key)
        if rv is None:
            user_info = auth.get_userinfo_with_token()
            rv = user_info['email']
            cache.set(cache_key, rv, timeout=60 * 50)

        response = get_transaction_history_for_user_and_product(rv, id)
        return response, 200

    @auth.requires_auth
    @api.expect(transaction)
    def put(self, id):
        cache_key = CACHE_PREFIX + request.headers.get("Authorization", None)
        rv = cache.get(cache_key)
        if rv is None:
            user_info = auth.get_userinfo_with_token()
            rv = user_info['email']
            cache.set(cache_key, rv, timeout=60 * 50)

        data = request.json
        upsert_transaction(data, rv)
        return data, 200

    @auth.requires_auth
    @api.response(204, 'Transaction successfully deleted.')
    def delete(self, id):

        cache_key = CACHE_PREFIX + request.headers.get("Authorization", None)
        rv = cache.get(cache_key)
        if rv is None:
            user_info = auth.get_userinfo_with_token()
            rv = user_info['email']
            cache.set(cache_key, rv, timeout=60 * 50)

        request.json
        delete_transaction(rv, id)
        return None, 204
