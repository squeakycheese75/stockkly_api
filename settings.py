# Flask settings
# FLASK_SERVER_NAME = 'localhost:8888'
FLASK_DEBUG = True  # Do not use debug mode in production
FLASK_HOST = '0.0.0.0'
FLASK_PORT = '8888'

ARCTIC_HOST = '172.17.0.2'
ARCTIC_STORE = 'NASDAQ'

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# # SQLAlchemy settings
# SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
# SQLALCHEMY_TRACK_MODIFICATIONS = False
