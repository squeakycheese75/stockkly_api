import logging
from flask_restplus import Resource
from api.restplus import api
from api.shared.serialisers import price
import html
from cache import cache
from api.controllers.prices import get_price

log = logging.getLogger(__name__)

ns = api.namespace('prices', description='Operations related to Prices')

CACHE_PREFIX = 'historicalPrices:'


@ns.route('/<string:ticker>')
@api.response(404, 'Price not found.')
class PriceItem(Resource):
    @api.marshal_with(price)
    def get(self, ticker):
        """
        Returns the latest price
        """
        unecTicker = html.unescape(ticker)
        cache_key = CACHE_PREFIX + unecTicker
        rv = cache.get(cache_key)
        if rv is None:
            rv = get_price(unecTicker)
            cache.set(cache_key, rv, timeout=30)
        return rv, 200
