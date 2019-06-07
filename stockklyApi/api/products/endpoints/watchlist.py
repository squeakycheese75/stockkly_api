import logging
from flask_cors import cross_origin
from flask import request
from flask_restplus import Resource

from stockklyApi.api.restplus import api
from stockklyApi.api import auth
# from stockklyApi.api.products.repositories.prices import get_price, upsert_price, create_price
# from stockklyApi.api.products.serialisers import price

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
        # tList = tickers.split(",")
        response = [
            {
                "ccy": "USD",
                "change": 0.19,
                "id": "DIS",
                "movement": 0.08,
                "name": "Disney",
                "price": 133.04,
                "spot": 1.2922,
                "symbol": "$",
                "ticker": "DIS"
            },
            {
                "ccy": "USD",
                "change": 0.51,
                "id": "TSLA",
                "movement": 1.06,
                "name": "Tesla",
                "price": 206.98,
                "spot": 1.2922,
                "symbol": "$",
                "ticker": "TSLA"
            }
        ]
        # response = get_prices_for_list(tickers)
        return response, 200
