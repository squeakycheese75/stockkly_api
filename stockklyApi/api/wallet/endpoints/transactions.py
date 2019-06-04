from flask import Blueprint, render_template, request, jsonify
from flask_cors import cross_origin
from flask_restplus import Resource
import json
import logging
import datetime

from stockklyApi.api import auth
from stockklyApi.database.db import get_db
from stockklyApi.api.wallet.repositories.transactions import get_transaction_history_for_user_and_product, get_transaction_history_for_user
from stockklyApi.api.wallet.serializers import transaction

from stockklyApi.api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace('wallet/transactions', description='Operations related to wallet Transactions')


# @cross_origin(headers=['Content-Type', 'Authorization'], origin='*', allow_headers='*')
# @auth.requires_auth
@ns.route('/')
class TransactionCollection(Resource):
    @auth.requires_auth
    @api.marshal_list_with(transaction)
    def get(self):
        """
        Returns list of all transactions for an authenticated user.
        """
        # Get email from AccessToken
        token = auth.get_Token()
        userInfo = auth.get_userinfo_with_token()
        userEmail = userInfo['email']

        # userEmail = 'james_wooltorton@hotmail.com'
        # ticker = 'MSFT'
        # response = get_transaction_history_for_user_and_product(userEmail, ticker)
        response = get_transaction_history_for_user(userEmail)
        #  I know but if i don't  do this it runs through dumps twice
        resval = json.loads(response)
        return resval, 200

    @api.response(201, 'Category successfully created.')
    @api.expect(transaction)
    def post(self):
        """
        Creates a new blog category.
        """
        data = request.json
        # create_transacion(data)
        return None, 201


@ns.route('/<string:id>')
@api.response(404, 'Category not found.')
class TransactionItem(Resource):
    @auth.requires_auth
    @api.marshal_list_with(transaction)
    def get(self, id):
        """
        Returns list of products transactions for an authenticated user.
        """
        # Get email from AccessToken
        token = auth.get_Token()
        userInfo = auth.get_userinfo_with_token()
        userEmail = userInfo['email']

        response = get_transaction_history_for_user_and_product(userEmail, id)
        #  I know but if i don't  do this it runs through dumps twice
        resval = json.loads(response)
        return resval, 200

    @api.expect(transaction)
    def put(self, id):
        """
        Updates a blog category.

        Use this method to change the name of a blog category.

        * Send a JSON object with the new name in the request body.

        ```
        {
          "name": "New Category Name"
        }
        ```

        * Specify the ID of the category to modify in the request URL path.
        """
        data = request.json
        # update_transacion(id, data)
        return None, 204

    @api.response(204, 'Category successfully deleted.')
    def delete(self, id):
        """
        Deletes blog category.
        """
        # delete_category(id)
        return None, 204
