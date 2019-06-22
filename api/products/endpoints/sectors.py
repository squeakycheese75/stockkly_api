import logging
from flask_cors import cross_origin
from flask import request
from flask_restplus import Resource

from api.restplus import api
from api import auth
from cache import cache

log = logging.getLogger(__name__)

ns = api.namespace('products/sectors', description='Operations related to Product sectors')


@ns.route('/')
class SectorCollection(Resource):
    # @auth.requires_auth
    def get(self):
        rv = cache.get('sectorsList')
        if rv is None:
            rv = ["Precious metals"]
            cache.set('sectorsList', rv, timeout=5 * 60)
        # resval = ["Equity", "Crypto", "Precious metals"]
        return rv, 200
