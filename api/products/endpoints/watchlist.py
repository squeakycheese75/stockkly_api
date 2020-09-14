import logging
from flask_restplus import Resource
from api.restplus import api
from api.products.business import watchlist

log = logging.getLogger(__name__)

ns = api.namespace('watchlist', description='Operations related to Watchlist')


@ns.route('/<string:tickers>')
@api.response(404, 'Watchlist items not found.')
class WatchListItem(Resource):
    def get(self, tickers) -> dict:
        """
        Returns a list of Products that are in a watchlist.
        """
        response = []
        tickerList = tickers.split(",")
        for item in tickerList:
            resval = watchlist.get_ticker(item.upper().strip())
            if resval is not None:
                response.append(resval)
        return response, 200
