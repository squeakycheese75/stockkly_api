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


log = logging.getLogger(__name__)

ns = api.namespace('products/prices', description='Operations related to Prices sectors')

# load the mongo connection
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
MONGO_CONNECTION = env.get("MONGO_CONNECTION")

# Initialise
config = {
    "client": MONGO_CONNECTION,
    'db': 'stockkly',
    'collection': 'prices'
}
priceRepo = stockkly_repo.prices(config)


# @ns.route('/')
# class PricesCollection(Resource):
#     @api.response(201, 'Price successfully created.')
#     @api.expect(price)
#     # @auth.requires_auth
#     def post(self):
#         """
#         Creates a new product
#         """
#         data = request.json
#         # create_price(data)
#         # price.upsert_price_with_data()
#         return None, 201


@ns.route('/<string:ticker>')
@api.response(404, 'Price not found.')
class PriceItem(Resource):
    @api.marshal_with(price)
    def get(self, ticker):
        """
        Returns list of Product
        """

        unecTicker = html.unescape(ticker)
        cache_key = 'price:' + unecTicker
        rv = cache.get(cache_key)
        if rv is None:
            rv = priceRepo.get_price_now(unecTicker)
            cache.set(cache_key, rv, timeout=30)
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
