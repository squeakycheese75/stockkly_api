import logging
import json
from flask import request
from flask_restplus import Resource
from api.repositories.products_repo import upsert_product, get_products, create_product, get_product
from api.shared.serialisers import product
from api.restplus import api
from cache import cache

log = logging.getLogger(__name__)

ns = api.namespace('products', description='Operations related to Product data')

CACHE_PREFIX = 'product:'


@ns.route('/')
class ProductCollection(Resource):
    @api.marshal_list_with(product)
    def get(self):
        """
        Returns a list of Products
        """
        rv = cache.get('productList')
        if rv is None:
            response = get_products()
            rv = json.loads(response)
            cache.set('productList', rv, timeout=60 * 60)
        return rv, 200

    @api.response(201, 'Product successfully created.')
    @api.expect(product)
    # @auth.requires_auth
    def post(self):
        """
        Creates a new Product
        """
        data = request.json
        create_product(data)
        return None, 201


@ns.route('/<string:id>')
@api.response(404, 'Product not found.')
class ProductItem(Resource):

    @api.marshal_with(product)
    def get(self, id):
        """
        Returns a single Product
        """
        cache_key = CACHE_PREFIX + id
        rv = cache.get(cache_key)
        if rv is None:
            rv = get_product(id)
            cache.set(cache_key, rv, timeout=60 * 60)
        return rv, 200

    @api.expect(product)
    def put(self, id):
        """
        Updates a Produc
        """
        data = request.json
        upsert_product(data, id)
        return None, 204
