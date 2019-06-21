import logging
from flask_cors import cross_origin
from flask import request
from flask_restplus import Resource

from api.restplus import api
from api import auth

log = logging.getLogger(__name__)

ns = api.namespace('products/sectors', description='Operations related to Product sectors')


@ns.route('/')
class SectorCollection(Resource):
    # @auth.requires_auth
    # @api.marshal_list_with(transaction)
    def get(self):
        resval = ["Equity", "Crypto", "Precious metals"]
        # resval = json.loads(response)
        return resval, 200
