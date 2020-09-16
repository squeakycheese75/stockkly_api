import logging
from flask import request
from flask_restplus import Resource
from api.repositories.users_repo import get_user, create_user, upsert_user
from api.shared.serialisers import user
from api.restplus import api
from api import auth

log = logging.getLogger(__name__)

ns = api.namespace('profile', description='Operations related to user data')

default_ticker = []


@ns.route('/')
class ProfileCollection(Resource):
    @api.marshal_list_with(user)
    @auth.requires_auth
    def get(self):
        userInfo = auth.get_userinfo_with_token()
        userEmail = userInfo['email']
        response = get_user(userEmail)
        if response is None:
            # Create new profile with defaults
            response = {
                "watchList": default_ticker,
                "currency": "GBP",
                "symbol": "£",
                "refreshRate": 30,
                "devmode": False
            }
            create_user(response, userEmail)
        else:
            response['id'] = str(response["_id"])

        return response, 200

    @api.response(201, 'Profile successfully created.')
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

    @auth.requires_auth
    @api.expect(user)
    def put(self):
        userInfo = auth.get_userinfo_with_token()
        userEmail = userInfo['email']

        data = request.json
        upsert_user(data, userEmail)
        return data, 200

    # @api.response(204, 'Category successfully deleted.')
    # def delete(self, id):
    #     """
    #     Deletes blog category.
    #     """
    #     # delete_category(id)
    #     return None, 204
