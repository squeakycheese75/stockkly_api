import logging
from flask_cors import cross_origin
from flask import request
from flask_restplus import Resource

from stockklyApi.api.restplus import api
from stockklyApi.api import auth
from stockklyApi.api.products.repositories.prices import get_price, upsert_price, create_price
from stockklyApi.api.products.serialisers import price

log = logging.getLogger(__name__)

ns = api.namespace('products/prices', description='Operations related to Prices sectors')


@ns.route('/')
class PricesCollection(Resource):
    @api.response(201, 'Price successfully created.')
    @api.expect(price)
    # @auth.requires_auth
    def post(self):
        """
        Creates a new product
        """
        data = request.json
        create_price(data)
        return None, 201


@ns.route('/<string:id>')
@api.response(404, 'Price not found.')
class PriceItem(Resource):
    @api.marshal_with(price)
    def get(self, id):
        """
        Returns list of Product
        """
        response = get_price(id)
        return response, 200

    # @auth.requires_auth
    @api.expect(price)
    def put(self, id):
        data = request.json
        upsert_price(data, id)
        return None, 204
