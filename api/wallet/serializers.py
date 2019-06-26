from flask_restplus import fields
from api.restplus import api

# blog_post = api.model('Blog post', {
#     'id': fields.Integer(readOnly=True, description='The unique identifier of a blog post'),
#     'title': fields.String(required=True, description='Article title'),
#     'body': fields.String(required=True, description='Article content'),
#     'pub_date': fields.DateTime,
#     'category_id': fields.Integer(attribute='category.id'),
#     'category': fields.String(attribute='category.name'),
# })

# pagination = api.model('A page of results', {
#     'page': fields.Integer(description='Number of this page of results'),
#     'pages': fields.Integer(description='Total number of pages of results'),
#     'per_page': fields.Integer(description='Number of items per page of results'),
#     'total': fields.Integer(description='Total number of results'),
# })

# page_of_blog_posts = api.inherit('Page of blog posts', pagination, {
#     'items': fields.List(fields.Nested(blog_post))
# })

# category = api.model('Blog category', {
#     'id': fields.Integer(readOnly=True, description='The unique identifier of a blog category'),
#     'name': fields.String(required=True, description='Category name'),
# })

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
    '_id': fields.String,
    'owner': fields.String,
    'ticker': fields.String,
    'transdate': fields.DateTime,
    'transtype': fields.String,
    'quantity': fields.Float,
    'price': fields.Float,
    #             'transdate': request_data['transdate'],
    #             'transtype': request_data['transtype'],
    #             'quantity': request_data['quantity'],
    #             'price': request_data['price'],
    #             'details': request_data['details'],
})

# category_with_posts = api.inherit('Blog category with posts', category, {
#     'posts': fields.List(fields.Nested(blog_post))
# })
