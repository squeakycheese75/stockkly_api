from flask import current_app, g
from flask.cli import with_appcontext
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from os import environ as env
import logging
import pymongo

log = logging.getLogger(__name__)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
MONGO_CONNECTION = env.get("MONGO_CONNECTION")


def get_db():
    if 'db' not in g:
        # Connect to Local MONGODB
        try:
            # g.db = None
            log.info('Opening MongoDb connection')
            g.db = MongoClient(
                MONGO_CONNECTION)
            db_info = g.db.server_info()
            #db_info = g.db['stockkly']
        except (pymongo.errors.ConnectionFailure, pymongo.errors.ServerSelectionTimeoutError,  pymongo.errors.OperationFailure) as e:
            log.error("Could not connect to server: %s" % e)
            g.db = None
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        log.info('Closing MongoDb connection')
        db.close()
