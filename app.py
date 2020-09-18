from flask import Flask, Blueprint
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from os import environ as env
import os
import logging.config
import settings
from api.restplus import api
from api.mongo import mongoDB
from waitress import serve
from werkzeug.middleware.proxy_fix import ProxyFix
from api.endpoints.prices import ns as product_prices_namespace
from api.endpoints.prices_historical import ns as pricesHistorical_namespace
from api.endpoints.products import ns as products_namespace
from api.endpoints.profile import ns as profile_users_namespace
from api.endpoints.transactions import ns as wallet_transactions_namespace
from api.endpoints.holdings import ns as wallet_holdings_namespace
from api.endpoints.watchlist import ns as product_watchlist_namespace


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
MONGO_CONNECTION = env.get("MONGO_CONNECTION")
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

app.config["MONGO_URI"] = MONGO_CONNECTION
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)
CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "False"}})


def configure_app(flask_app):
    flask_app.config["MONGO_URI"] = MONGO_CONNECTION


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(wallet_holdings_namespace)
    api.add_namespace(wallet_transactions_namespace)
    api.add_namespace(products_namespace)
    api.add_namespace(product_prices_namespace)
    api.add_namespace(profile_users_namespace)
    api.add_namespace(product_watchlist_namespace)
    api.add_namespace(pricesHistorical_namespace)

    flask_app.register_blueprint(blueprint)
    mongoDB.init_app(app)


def main():
    if(settings.FLASK_PRODUCTION_MODE):
        log.info('Running in Production Mode')
        serve(app,  host=settings.FLASK_HOST, port=settings.FLASK_PORT)
    else:
        log.info('Running in Development Mode')
        app.run(host=settings.FLASK_HOST,
                port=settings.FLASK_PORT,
                debug=settings.FLASK_DEBUG,
                threaded=True)


initialize_app(app)

if __name__ == "__main__":
    main()
