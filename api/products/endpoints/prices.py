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

from api.products.repositories.prices import get_price_latest, get_price_now
from api.products.business.prices import get_historical, get_price

log = logging.getLogger(__name__)

ns = api.namespace('prices', description='Operations related to Prices sectors')

@ns.route('/<string:ticker>')
@api.response(404, 'Price not found.')
class PriceItem(Resource):
    @api.marshal_with(price)
    def get(self, ticker):
        """
        Returns the latest price
        """
        unecTicker = html.unescape(ticker)
        cache_key = 'price:' + unecTicker
        rv = cache.get(cache_key)
        if rv is None:
            rv = get_price(unecTicker)
            cache.set(cache_key, rv, timeout=30)
        return rv, 200
