import logging
from flask_cors import cross_origin
from flask import request
from flask_restplus import Resource
from api.wallet.business.holdings import get_holdings, get_holding, get_holdings_historical
from api.wallet.serializers import holding
from api.restplus import api
from api import auth
from cache import cache


log = logging.getLogger(__name__)

ns = api.namespace('wallet', description='Operations related to wallet Holdings')


@ns.route('/')
class HoldingsCollection(Resource):
    @api.marshal_list_with(holding)
    @auth.requires_auth
    def get(self):
        """
        Returns list of Holdings
        """
        # auth = request.headers.get("Authorization", None)

        # print(auth)
        cache_key = 'auth:' + request.headers.get("Authorization", None)
        rv = cache.get(cache_key)
        if rv is None:
            userInfo = auth.get_userinfo_with_token()
            rv = userInfo['email']
            cache.set(cache_key, rv, timeout=60 * 50)
        # return rv, 200

        response = get_holdings(rv)
        return response, 200


@ns.route('/<string:ticker>')
@api.response(404, 'Product not found.')
class HoldingItem(Resource):
    @auth.requires_auth
    @api.marshal_with(holding)
    def get(self, ticker):
        """
        Returns list of Holdings
        # """
        cache_key = 'auth:' + request.headers.get("Authorization", None)
        rv = cache.get(cache_key)
        if rv is None:
            userInfo = auth.get_userinfo_with_token()
            rv = userInfo['email']
            cache.set(cache_key, rv, timeout=60 * 50)

        response = get_holding(rv, ticker)
        return response, 200


# @api.marshal_list_with(holding)
@auth.requires_auth
@ns.route('/historical/')
class HistoricalHoldings(Resource):
    def get(self):
        cache_key = 'auth:' + request.headers.get("Authorization", None)
        rv = cache.get(cache_key)
        if rv is None:
            userInfo = auth.get_userinfo_with_token()
            rv = userInfo['email']
            cache.set(cache_key, rv, timeout=60 * 50)
        response = get_holdings_historical("test")
        return response, 200
