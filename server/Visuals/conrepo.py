from flask import Flask,request,jsonify
from flask_cors import CORS
from flask import render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)
CORS(app)
# Database Connection
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME='gCodexDB'
COLLECTION_NAME = 'LinesOfCode'

FIELDS = {'branch': True, 'Commits': True,'_id': False}


def donorschoose_projects():
    
  
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.find(projection=FIELDS)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects

x=donorschoose_projects

print(type(x))