import logging
from flask_cors import cross_origin
from flask import request
from flask_restplus import Resource
from stockklyApi.api.wallet.business.holdings import get_holdings, get_holding
from stockklyApi.api.wallet.serializers import holding
from stockklyApi.api.restplus import api
from stockklyApi.api import auth


log = logging.getLogger(__name__)

ns = api.namespace('wallet/holdings', description='Operations related to wallet Holdings')


@ns.route('/')
class HoldingsCollection(Resource):
    @api.marshal_list_with(holding)
    @auth.requires_auth
    def get(self):
        """
        Returns list of blog categories.
        """
        # userEmail = 'james_wooltorton@hotmail.com'
        userInfo = auth.get_userinfo_with_token()
        userEmail = userInfo['email']

        response = get_holdings(userEmail)
        return response, 200


@ns.route('/<string:ticker>')
@api.response(404, 'Product not found.')
class HoldingItem(Resource):
    # @auth.requires_auth
    @api.marshal_with(holding)
    def get(self, ticker):
        """
        Returns list of Product
        # """
        # userInfo = auth.get_userinfo_with_token()
        # userEmail = userInfo['email']
        userEmail = "james_wooltorton@hotmail.com"

        response = get_holding(userEmail, ticker)
        return response, 200
