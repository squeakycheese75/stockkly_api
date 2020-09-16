from flask_restplus import fields
from api.restplus import api

holding = api.model('Holding', {
    'ticker': fields.String,
    'name': fields.String,
    'change': fields.Float,
    'price':  fields.Float,
    'movement':  fields.Float,
    'qty':  fields.Float,
    'total': fields.Float,
    'spot': fields.Float,
    'ccy': fields.String,
    'symbol': fields.String,
    'total_change': fields.Float,
    'displayTicker': fields.String
})


balance = api.model('Balance', {
    'ticker': fields.String,
    'qty': fields.Float,
})

transaction = api.model('Transaction', {
    'id': fields.String,
    'ticker': fields.String,
    'transdate': fields.DateTime,
    'transtype': fields.String,
    'quantity': fields.Float,
    'price': fields.Float,
    'details': fields.String
})

company = api.model('Company', {
    'name': fields.String,
    'url': fields.String,
})

quote = api.model('Quote', {
    'symbol': fields.String,
    'currency': fields.String,
})

icon = api.model('Icon', {
    'path': fields.String,
    'width': fields.Integer,
})

product = api.model('Product', {
    'ticker': fields.String,
    'displayTicker': fields.String,
    'name': fields.String,
    'description': fields.String,
    'company': fields.Nested(company),
    'sector': fields.String,
    'quote':  fields.Nested(quote),
    "exchange": fields.String,
})


price = api.model('Price', {
    'ticker': fields.String,
    'open': fields.Float,
    'change': fields.Float,
    'price':  fields.Float,
    'movement':  fields.Float,
    'priceDate': fields.DateTime,
    'symbol': fields.String
})

user = api.model('User', {
    'id': fields.String,
    'currency': fields.String,
    'symbol': fields.String,
    'refreshRate': fields.Integer,
    'watchList': fields.List(fields.String),
    'devmode': fields.Boolean
})
