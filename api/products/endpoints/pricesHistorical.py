import logging
from flask_cors import cross_origin
from flask import request
from flask_restplus import Resource
from dotenv import load_dotenv, find_dotenv
from os import environ as env

from api.restplus import api
from api import auth
from api.products.serialisers import price
import stockkly_repo
import html
from cache import cache
import json

from api.products.repositories.prices import get_price_now
from api.products.business.prices import get_historical


log = logging.getLogger(__name__)

ns = api.namespace('pricesHistorical', description='Operations related to Prices sectors')


@ns.route('/<string:ticker>')
@api.response(404, 'PricesHistorical not found.')
class HistoricalPrices(Resource):

    # @api.marshal_with(product)
    def get(self, ticker):
        """
        Returns a list of historical prices for charting
        """
        unecTicker = html.unescape(ticker)
        cache_key = 'historicalPrices:' + unecTicker
        rv = cache.get(cache_key)
        if rv is None:
            response = get_historical(unecTicker, 90)
            cache.set(cache_key, rv, timeout=60 * 60)
            rv = response
        return rv, 200


# # @auth.requires_auth
# @api.expect(price)
# def put(self, ticker):
#     data = request.json
#     upsert_price(data, ticker)
#     return None, 204

# @api.expect(price)
# def post(self, ticker):
#     """
#     Creates a new product
#     """
#     data = request.json
#     # create_price(data)
#     price.upsert_price_with_data(id, data)
#     return None, 201
