from flask_restplus import fields
from api.restplus import api

holding = api.model('Holding', {
    # 'id': fields.Integer(readOnly=True, description='The unique identifier of a blog category'),
    # 'name': fields.String(required=True, description='Category name'),
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
    # 'id': fields.Integer(readOnly=True, description='The unique identifier of a blog category'),
    # 'name': fields.String(required=True, description='Category name'),
    # 'owner':  fields.String,
    # 'id': fields.Integer(readOnly=True, description='The unique identifier of a blog category'),
    'id': fields.String,
    # 'owner': fields.String,
    'ticker': fields.String,
    'transdate': fields.DateTime,
    'transtype': fields.String,
    'quantity': fields.Float,
    'price': fields.Float,
    'details': fields.String
    #             'transdate': request_data['transdate'],
    #             'transtype': request_data['transtype'],
    #             'quantity': request_data['quantity'],
    #             'price': request_data['price'],
    #             'details': request_data['details'],
})

# category_with_posts = api.inherit('Blog category with posts', category, {
#     'posts': fields.List(fields.Nested(blog_post))
# })
