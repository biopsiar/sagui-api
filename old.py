from flask import Flask, jsonify, Response
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

client = MongoClient("mongodb://root:example@mongo/?authSource=admin")
db = client.sagui

@app.route("/")
def index():
    return 'SAGUI v1.0'

@app.route("/items", methods=['GET'])
def find_many_products():
    """ Retorna JSON com todos os produtos no banco de dados """
    _products = db.items.find()
    # products = [product for product in _products]
    
    return Response(dumps(_products), mimetype='application/json')