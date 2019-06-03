import logging
from flask_cors import cross_origin
from flask import request
from flask_restplus import Resource

from stockklyApi.api.products.business.info import get_product, upsert_product
from stockklyApi.api.products.serialisers import product

from stockklyApi.api.restplus import api
from stockklyApi.api import auth

log = logging.getLogger(__name__)

ns = api.namespace('products/info', description='Operations related to Product Info')


@cross_origin(headers=['Content-Type', 'Authorization'], origin='*', allow_headers='*')
# @auth.requires_auth
@ns.route('/')
class ProductCollection(Resource):
    # @auth.requires_auth
    @api.response(201, 'Category successfully created.')
    @api.expect(product)
    def post(self):
        """
        Creates a new product
        """
        data = request.json
        upsert_product(data)
        return None, 201


@ns.route('/<string:id>')
@api.response(404, 'Product not found.')
class ProductItem(Resource):
    # @auth.requires_auth
    @api.marshal_with(product)
    def get(self, id):
        """
        Returns list of Product
        """
        response = get_product(id)
        return response, 200

    @api.expect(product)
    def put(self, id):
        data = request.json
        upsert_product(data)
        return None, 204

    # @api.response(204, 'Category successfully deleted.')
    # def delete(self, id):
    #     """
    #     Deletes blog category.
    #     """
    #     # delete_category(id)
    #     return None, 204
