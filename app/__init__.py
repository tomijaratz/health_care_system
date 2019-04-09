import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo


class JSONEncoder(json.JSONEncoder):
    """ extend json-encoder class"""

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


# creating the flask app
app = Flask(__name__)

# adding mongo url to flask config
app.config['MONGO_URI'] = os.environ.get('DB')
mongo = PyMongo(app)

# json encoder class for handling ObjectId & datetime object
app.json_encoder = JSONEncoder

from app.controllers import *