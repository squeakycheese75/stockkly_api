from flask import Flask, Blueprint
from flask_restplus import Resource, Api
from flask_cors import CORS

import os
import logging.config
from stockklyApi import settings
from stockklyApi.api.restplus import api
# from stockklyApi.api.wallet.endpoints.categories import ns as blog_categories_namespace
from stockklyApi.api.wallet.endpoints.holdings import ns as wallet_holdings_namespace
from stockklyApi.api.wallet.endpoints.transactions import ns as wallet_transactions_namespace


app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

# CORS(app, expose_headers='Authorization', supports_credentials=True)
CORS(app)
# api = Api(app)  # Create a Flask-RESTPlus API


@api.route('/hello')  # Create a URL route to this resource
class HelloWorld(Resource):  # Create a RESTful resource
    def get(self):  # Create GET endpoint
        return {'hello': 'world'}


def initialize_app(flask_app):
    # configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(flask_app)
    api.init_app(blueprint)
    # app.register_blueprint(blueprint)
    api.add_namespace(wallet_holdings_namespace)
    api.add_namespace(wallet_transactions_namespace)

    # api.add_namespace(transactions_api)
    flask_app.register_blueprint(blueprint)

    # db.init_app(flask_app)


# if __name__ == '__main__':
#     # app.run(debug=True)  # Start a development server
#     initialize_app(app)
#     logging.basicConfig(filename='error.log', level=logging.DEBUG)
#     # log.info(
#     #     '>>>>> Starting development server at http://{}:5000/api/ <<<<<'.format(settings.FLASK_HOST))
#     app.run(host=settings.FLASK_HOST, port=settings.FLASK_PORT, debug=settings.FLASK_DEBUG)

def main():
    initialize_app(app)
    log.info(
        '>>>>> Starting development server at http://{}:5000/api/ <<<<<'.format(settings.FLASK_HOST))
    # app.run(debug=settings.FLASK_DEBUG)
    # app.run(host=settings.FLASK_HOST, port=settings.FLASK_PORT, debug=settings.FLASK_DEBUG)


# if __name__ == "__main__":
main()
