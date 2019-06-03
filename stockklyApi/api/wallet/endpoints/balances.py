import logging
from flask_cors import cross_origin
from flask import request
from flask_restplus import Resource
from stockklyApi.api.wallet.repositories.balances import create_balance, update_balance
from stockklyApi.api.wallet.serializers import balance
from stockklyApi.api.restplus import api
from stockklyApi.api import auth


log = logging.getLogger(__name__)

ns = api.namespace('wallet/balances', description='Operations related to wallet balances')


@ns.route('/')
class HoldingsCollection(Resource):
    @api.response(201, 'Category successfully created.')
    @api.expect(balance)
    def post(self):
        """
        Creates a new blog category.
        """
        # userEmail = 'james_wooltorton@hotmail.com'
        userInfo = auth.get_userinfo_with_token()
        userEmail = userInfo['email']

        data = request.json
        create_balance(userEmail, data)
        return None, 201


@ns.route('/<string:id>')
@api.response(404, 'Product not found.')
class BalanceItem(Resource):
    # @auth.requires_auth
    @api.expect(balance)
    def put(self, id):
        data = request.json
        userInfo = auth.get_userinfo_with_token()
        userEmail = userInfo['email']
        # userEmail = 'james_wooltorton@hotmail.com'
        ticker = data['ticker']
        qty = data['qty']
        update_balance(userEmail, ticker, qty)
        return None, 204
