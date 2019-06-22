from flask import Flask, Blueprint
from flask_restplus import Resource, Api
from flask_cors import CORS

import os
import logging.config
import settings
from api.restplus import api

from api.wallet.endpoints.holdings import ns as wallet_holdings_namespace
from api.wallet.endpoints.transactions import ns as wallet_transactions_namespace
from api.wallet.endpoints.balances import ns as wallet_balances_namespace
from api.products.endpoints.info import ns as product_info_namespace
from api.products.endpoints.sectors import ns as product_sectors_namespace
from api.products.endpoints.prices import ns as product_prices_namespace
from api.profile.endpoints.user import ns as profile_users_namespace
from api.products.endpoints.watchlist import ns as product_watchlist_namespace


app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)
CORS(app)

# CORS(app, expose_headers='Authorization', supports_credentials=True)

# api = Api(app)  # Create a Flask-RESTPlus API


def initialize_app(flask_app):
    # configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(flask_app)
    api.init_app(blueprint)
    # app.register_blueprint(blueprint)
    api.add_namespace(wallet_holdings_namespace)
    api.add_namespace(wallet_transactions_namespace)
    api.add_namespace(wallet_balances_namespace)
    api.add_namespace(product_info_namespace)
    api.add_namespace(product_sectors_namespace)
    api.add_namespace(product_prices_namespace)
    api.add_namespace(profile_users_namespace)
    api.add_namespace(product_watchlist_namespace)

    # api.add_namespace(transactions_api)
    flask_app.register_blueprint(blueprint)

    # db.init_app(flask_app)


# def main():
initialize_app(app)
# log.info('RUnning')
# log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
# app.run(debug=settings.FLASK_DEBUG)
# app.run(host=settings.FLASK_HOST, port=settings.FLASK_PORT,
#         debug=settings.FLASK_DEBUG)


# if __name__ == "__main__":
#     main()
