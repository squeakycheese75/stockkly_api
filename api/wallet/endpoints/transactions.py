from flask import Blueprint, render_template, request, jsonify
from flask_cors import cross_origin
from flask_restplus import Resource
import json
import logging
import datetime

from api import auth
from database.db import get_db
from api.wallet.repositories.transactions import get_transaction_history_for_user_and_product, get_transaction_history_for_user
from api.wallet.serializers import transaction
from api.wallet.business.transaction import upsert_transaction, create_transaction
from cache import cache

from api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace('wallet/transactions', description='Operations related to wallet Transactions')


@ns.route('/')
class TransactionCollection(Resource):
    @auth.requires_auth
    @api.marshal_list_with(transaction)
    def get(self):
        """
        Returns list of all transactions for an authenticated user.
        """
        # Get email from AccessToken
        # token = auth.get_Token()
        # userInfo = auth.get_userinfo_with_token()
        # userEmail = userInfo['email']

        cache_key = 'auth:' + request.headers.get("Authorization", None)
        rv = cache.get(cache_key)
        if rv is None:
            userInfo = auth.get_userinfo_with_token()
            rv = userInfo['email']
            cache.set(cache_key, rv, timeout=60 * 50)

        response = get_transaction_history_for_user(rv)
        #  I know but if i don't  do this it runs through dumps twice
        resval = json.loads(response)
        return resval, 200

    @api.response(201, 'Transaction successfully created.')
    @api.expect(transaction)
    def post(self):
        userInfo = auth.get_userinfo_with_token()
        userEmail = userInfo['email']

        data = request.json
        response = create_transaction(data, userEmail)

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
        # Get email from AccessToken
        # token = auth.get_Token()
        # userInfo = auth.get_userinfo_with_token()
        # userEmail = userInfo['email']
        cache_key = 'auth:' + request.headers.get("Authorization", None)
        rv = cache.get(cache_key)
        if rv is None:
            userInfo = auth.get_userinfo_with_token()
            rv = userInfo['email']
            cache.set(cache_key, rv, timeout=60 * 50)

        response = get_transaction_history_for_user_and_product(rv, id)
        #  I know but if i don't  do this it runs through dumps twice
        resval = json.loads(response)
        return resval, 200

    @auth.requires_auth
    @api.expect(transaction)
    def put(self, id):
        # userInfo = auth.get_userinfo_with_token()
        # userEmail = userInfo['email']
        cache_key = 'auth:' + request.headers.get("Authorization", None)
        rv = cache.get(cache_key)
        if rv is None:
            userInfo = auth.get_userinfo_with_token()
            rv = userInfo['email']
            cache.set(cache_key, rv, timeout=60 * 50)

        data = request.json
        record_updated = upsert_transaction(data, rv)
        return None, 204

    @api.response(204, 'Transaction successfully deleted.')
    def delete(self, id):
        """
        Deletes blog category.
        """
        # delete_transaction(id)
        return None, 204
