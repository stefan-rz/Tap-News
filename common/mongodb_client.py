import os
import sys

from pymongo import MongoClient
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

from config import Config as cfg
cf = cfg().load_config_file()['common']

MONGO_DB_HOST = cf['MONGO_DB_HOST']
MONGO_DB_PORT = cf['MONGO_DB_PORT']
DB_NAME = cf['DB_NAME']

client = MongoClient("%s:%s" % (MONGO_DB_HOST, MONGO_DB_PORT))

def get_db(db=DB_NAME):
    db = client[db]
    return db
