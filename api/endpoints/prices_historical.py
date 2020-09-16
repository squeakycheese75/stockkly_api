import logging
from flask_restplus import Resource
from api.restplus import api
import html
from cache import cache
from api.controllers.prices import get_historical


log = logging.getLogger(__name__)

ns = api.namespace('pricesHistorical', description='Operations related to Historical Prices')


CACHE_PREFIX = 'historicalPrices:'


@ns.route('/<string:ticker>')
@api.response(404, 'PricesHistorical not found.')
class HistoricalPrices(Resource):
    # @api.marshal_with(prices)
    def get(self, ticker):
        """
        Returns a list of historical prices for charting
        """
        unecTicker = html.unescape(ticker)
        cache_key = CACHE_PREFIX + unecTicker
        rv = cache.get(cache_key)
        if rv is None:
            response = get_historical(unecTicker, 90)
            cache.set(cache_key, rv, timeout=60 * 60)
            rv = response
        return rv, 200
