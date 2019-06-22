import logging
from flask_cors import cross_origin
from flask import request
from flask_restplus import Resource
import json

from api.profile.repository.users import get_user, create_user, upsert_user
from api.profile.serialisers import user

from api.restplus import api
from api import auth

log = logging.getLogger(__name__)

ns = api.namespace('profile/user', description='Operations related to user data')

default_ticker = ["MSFT", "AAPL"]


@ns.route('/')
class ProductCollection(Resource):
    @api.marshal_list_with(user)
    @auth.requires_auth
    def get(self):
        # userId = 'james_wooltorton@hotmail.com'
        # get username from token
        userInfo = auth.get_userinfo_with_token()
        userEmail = userInfo['email']

        response = get_user(userEmail)
        if response is None:
            # Create new profile with defaults
            response = {
                # "userId": userEmail,
                "watchList": default_ticker,
                "currency": "GBP",
                "symbol": "£",
                "refreshRate": 30
            }
            create_user(response, userEmail)
        return response, 200

    @api.response(201, 'Category successfully created.')
    @api.expect(user)
    @auth.requires_auth
    def post(self):
        """
        Creates a new product
        """
        userInfo = auth.get_userinfo_with_token()
        userEmail = userInfo['email']

        data = request.json
        create_user(data, userEmail)
        return None, 201


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

    @auth.requires_auth
    @api.expect(user)
    def put(self):
        userInfo = auth.get_userinfo_with_token()
        userEmail = userInfo['email']

        data = request.json
        record_updated = upsert_user(data, userEmail)
        return None, 204

    # @api.response(204, 'Category successfully deleted.')
    # def delete(self, id):
    #     """
    #     Deletes blog category.
    #     """
    #     # delete_category(id)
    #     return None, 204