import logging
import traceback

from flask_restplus import Api
import settings

log = logging.getLogger(__name__)

api = Api(version='1.0.1', 
          title='Stockkly API',
          description='A free, near real-time, RestAPI for providing price data for stocks (FTSE, NASDAQ), crypto-currencies, funds and Precious metals (GOLD, SILVER).')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500
