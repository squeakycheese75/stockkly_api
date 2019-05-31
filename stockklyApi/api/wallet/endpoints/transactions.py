from flask import Blueprint, render_template, request, jsonify
from flask_cors import cross_origin
from flask_restplus import Resource
import json
import logging
import datetime

from stockklyApi.api import auth
from stockklyApi.database.db import get_db
from stockklyApi.api.wallet.business.transactions import get_transaction_history_for_user_and_product
from stockklyApi.api.wallet.serializers import transaction

from stockklyApi.api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace('wallet/transactions', description='Operations related to wallet Transactions')


@cross_origin(headers=['Content-Type', 'Authorization'], origin='*', allow_headers='*')
# @auth.requires_auth
@ns.route('/')
class TransactionsCollection(Resource):
    @api.marshal_list_with(transaction)
    def get(self):
        """
        Returns list of blog categories.
        """
        # Get email from AccessToken
        # userInfo = auth.get_userinfo_with_token()
        # userEmail = userInfo['email']

        userEmail = 'james_wooltorton@hotmail.com'
        ticker = 'MSFT'
        response = get_transaction_history_for_user_and_product(userEmail, ticker)
        #  I know but if i don't  do this it runs through dumps twice
        resval = json.loads(response)
        return resval, 200


# @ns.route("/<ticker>", methods=['GET',  'OPTIONS'])
# @cross_origin(headers=['Content-Type', 'Authorization'], origin='*', allow_headers='*')
# @auth.requires_auth
# def private_transactions_load(ticker):


# def get(self):
#     try:
#         # Get email from AccessToken
#         userInfo = auth.get_userinfo_with_token()
#         userEmail = userInfo['email']

#         trans = get_transaction_history_for_user_and_product(userEmail, ticker)

#         return jsonify(message=trans), 200
#     except:
#         return jsonify(message="Error loading user transactions."), 500


# @ns.route("", methods=['POST'])
# @cross_origin(headers=['Content-Type', 'Authorization'], origin='*', allow_headers='*')
# @auth.requires_auth
# def insert_transaction():
#     try:
#         request_data = request.get_json()
#         userEmail = auth.get_userinfo_with_token()['email']

#         db = get_db()['stockkly']
#         transactionsCollection = db['transactions']

#         # handle empty lists
#         trans = {
#             "owner": userEmail,
#             'ticker': request_data['ticker'],
#             'transdate': request_data['transdate'],
#             'transtype': request_data['transtype'],
#             'quantity': request_data['quantity'],
#             'price': request_data['price'],
#             'details': request_data['details'],
#         }
#         resId = transactionsCollection.insert_one(trans)
#         response = "Inserted transaction"
#         return jsonify(response), 201
#     except:
#         response = "Error inserting transaction."
#         jsonify(response), 500
