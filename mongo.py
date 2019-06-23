from flask_pymongo import PyMongo
from os import environ as env

mongoDB = PyMongo()


def init(self, app):

    mongoDB.init_app(app)
