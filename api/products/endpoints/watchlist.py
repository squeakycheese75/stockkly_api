import logging
from flask_cors import cross_origin
from flask import request
from flask_restplus import Resource

from api.restplus import api
from api import auth
# from stockklyApi.api.products.repositories.prices import get_price, upsert_price, create_price
from api.products.business import watchlist

log = logging.getLogger(__name__)

ns = api.namespace('watchlist', description='Operations related to Watchlist')


@ns.route('/<string:tickers>')
@api.response(404, 'Prices not found.')
class WatchListItem(Resource):
    # @api.marshal_with(price)
    def get(self, tickers):
        """
        Returns list of Product
        """
        # response = get_price(id)
        response = []
        tickerList = tickers.split(",")
        for item in tickerList:
            resval = watchlist.get_ticker(item.upper().strip())
            if resval is not None:
                response.append(resval)
        # response = get_prices_for_list(tickers)
        return response, 200
