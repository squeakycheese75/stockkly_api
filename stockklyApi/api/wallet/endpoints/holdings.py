import logging
from flask_cors import cross_origin
from flask import request
from flask_restplus import Resource
# from stockklyApi.api.wallet.business import get_holdings
from stockklyApi.api.wallet.business.holdings import get_holdings
# create_category, delete_category, update_category
from stockklyApi.api.wallet.serializers import holding
# , category_with_posts
from stockklyApi.api.restplus import api
from stockklyApi.api import auth
# from rest_api_demo.database.models import Category

log = logging.getLogger(__name__)

ns = api.namespace('wallet/holdings', description='Operations related to wallet Holdings')


@ns.route('/')
# @cross_origin(headers=['Content-Type', 'Authorization'], origin='*', allow_headers='*')
class HoldingsCollection(Resource):
    @api.marshal_list_with(holding)
    # @cross_origin(headers=['Content-Type', 'Authorization'], origin='*', allow_headers='*')
    @auth.requires_auth
    def get(self):
        """
        Returns list of blog categories.
        """
        # userEmail = 'james_wooltorton@hotmail.com'
        userInfo = auth.get_userinfo_with_token()
        userEmail = userInfo['email']

        response = get_holdings(userEmail)
        return response, 200

    # @api.response(201, 'Category successfully created.')
    # # @api.expect(category)
    # def post(self):
    #     """
    #     Creates a new blog category.
    #     """
    #     data = request.json
    #     create_category(data)
    #     return None, 201


# @ns.route('/<int:id>')
# @api.response(404, 'Category not found.')
# class CategoryItem(Resource):

#     # @api.marshal_with(category_with_posts)
#     def get(self, id):
#         """
#         Returns a category with a list of posts.
#         """
#         return Category.query.filter(Category.id == id).one()

#     # @api.expect(category)
#     @api.response(204, 'Category successfully updated.')
#     def put(self, id):
#         """
#         Updates a blog category.

#         Use this method to change the name of a blog category.

#         * Send a JSON object with the new name in the request body.

#         ```
#         {
#           "name": "New Category Name"
#         }
#         ```

#         * Specify the ID of the category to modify in the request URL path.
#         """
#         data = request.json
#         update_category(id, data)
#         return None, 204

#     @api.response(204, 'Category successfully deleted.')
#     def delete(self, id):
#         """
#         Deletes blog category.
#         """
#         delete_category(id)
#         return None, 204
