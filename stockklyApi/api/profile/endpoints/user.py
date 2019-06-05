import logging
from flask_cors import cross_origin
from flask import request
from flask_restplus import Resource
import json

from stockklyApi.api.profile.repository.users import get_user
from stockklyApi.api.profile.serialisers import user

from stockklyApi.api.restplus import api
from stockklyApi.api import auth

log = logging.getLogger(__name__)

ns = api.namespace('user', description='Operations related to user data')


@ns.route('/')
class ProductCollection(Resource):
    @api.marshal_list_with(user)
    # @auth.requires_auth
    def get(self):
        userId = 'james_wooltorton@hotmail.com'
        response = get_user(userId)
        # resval = json.loads(response)
        return response, 200

    # @api.response(201, 'Category successfully created.')
    # @api.expect(product)
    # @auth.requires_auth
    # def post(self):
    #     """
    #     Creates a new product
    #     """
    #     data = request.json
    #     create_product(data)
    #     return None, 201


# @ns.route('/<string:id>')
# @api.response(404, 'Product not found.')
# class ProductItem(Resource):

#     @api.marshal_with(product)
#     def get(self, id):
#         """
#         Returns list of Product
#         """
#         response = get_product(id)
#         return response, 200

#     # @auth.requires_auth
#     @api.expect(product)
#     def put(self, id):
#         data = request.json
#         upsert_product(data, id)
#         return None, 204

    # @api.response(204, 'Category successfully deleted.')
    # def delete(self, id):
    #     """
    #     Deletes blog category.
    #     """
    #     # delete_category(id)
    #     return None, 204
