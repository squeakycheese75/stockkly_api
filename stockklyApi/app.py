from flask import Flask
from flask_restplus import Resource, Api

import logging.config
from stockklyApi import settings


app = Flask(__name__)  # Create a Flask WSGI application
api = Api(app)  # Create a Flask-RESTPlus API


@api.route('/hello')  # Create a URL route to this resource
class HelloWorld(Resource):  # Create a RESTful resource
    def get(self):  # Create GET endpoint
        return {'hello': 'world'}


if __name__ == '__main__':
    # app.run(debug=True)  # Start a development server
    # initialize_app(app)
    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    # log.info(
    #     '>>>>> Starting development server at http://{}:5000/api/ <<<<<'.format(settings.FLASK_HOST))
    app.run(host=settings.FLASK_HOST, port=settings.FLASK_PORT, debug=settings.FLASK_DEBUG)
