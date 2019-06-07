from flask_restplus import fields
from stockklyApi.api.restplus import api


profileSettings = api.model('ProfileSettings', {
    'profile': fields.String,
    'currency': fields.String,
    'symbol': fields.String,
    'refreshRate': fields.Integer
})

user = api.model('User', {
    'userId': fields.String,
    'watching': fields.List(fields.String),
    'settings': fields.List(fields.Nested(profileSettings)),
})
