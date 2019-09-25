from flask_restplus import fields
from api.restplus import api
# import pymongo


# class ObjectIdField(fields.Raw):
#     def format(self, value):
#         if isinstance(value, ObjectId):
#             return str(ObjectId)
#         else:
#             raise MarshallingError()


profileSettings = api.model('ProfileSettings', {
    # 'id': fields.Integer,
    '_id': fields.String,
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
    # 'id': fields.Integer,
    'id': fields.String,
    'currency': fields.String,
    'symbol': fields.String,
    'refreshRate': fields.Integer,
    'watchList': fields.List(fields.String),

})
