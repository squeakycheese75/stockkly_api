import logging
from http import HTTPStatus
from flask_restplus import Resource
from api.restplus import api
from api.controllers import watchlist

log = logging.getLogger(__name__)

ns = api.namespace('watchlist', description='Operations related to Watchlist')


@ns.route('/<string:tickers>')
@api.response(404, 'Watchlist items not found.')
class WatchListItem(Resource):
    def get(self, tickers) -> (dict, int):
        """
        Returns a list of Products that are in a watchlist.
        """
        response = []
        ticker_list = tickers.split(",")
        for item in ticker_list:
            resval = watchlist.get_ticker(item.upper().strip())
            if resval is not None:
                response.append(resval)
        return response, HTTPStatus.OK
