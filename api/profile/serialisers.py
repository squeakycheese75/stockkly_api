from flask_restplus import fields
from api.restplus import api


profileSettings = api.model('ProfileSettings', {
    'name': fields.String,
    'currency': fields.String,
    'symbol': fields.String,
    'refreshRate': fields.Integer,
    'watchList': fields.List(fields.String)
})

user = api.model('User', {
    # 'userId': fields.String,
    # 'watching': fields.List(fields.String),
    # 'settings': fields.List(fields.Nested(profileSettings)),
    'currency': fields.String,
    'symbol': fields.String,
    'refreshRate': fields.Integer,
    'watchList': fields.List(fields.String)
})
