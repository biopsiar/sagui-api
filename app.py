from flask import Flask, jsonify
from pymongo import MongoClient

import json
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://root:example@mongo/?authSource=admin")
db = client.sagui

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route("/")
def index():
    return 'SAGUI v1.0'

@app.route("/items", methods=['GET'])
# **Find many products**
def find_many_products():
    """ Retorna JSON com todos os produtos no banco de dados
	Ex.: /api/votes/items/
    """
    products = db.items.find()
    output = []
    for q in products:
        del q['_id']
        output.append(q)
    return jsonify(output)

@app.route("/items/<item_id>", methods=['GET'])
# **Find specific products**
def find_one_products(item_id):
    """ Retorna a descricao baseada no identificador do produto
	Ex.: /api/votes/ID_ITEM/
    """
    products = db.items.find_one({'product_source' : int(item_id)})
    return JSONEncoder().encode(products)

@app.route("/votes", methods=['GET'])
# **Find votes**
def find_votes():
    """ Retorna todos os votos registrados 
	Ex.: /api/votes/
    """
    products = db.items.find()
    output = []
    for q in products:
        output.append({'evaluated_neutral': q['evaluated_neutral'], 'evaluated_negative': q['evaluated_negative'], 'evaluated_positive': q['evaluated_positive'], 'product_source': q['product_source']})
    return jsonify(output)

@app.route("/votes/<item_id>/<vote_type>/<user_id>", methods = ['GET'])
# **Update votes**
def update_votes(vote_type, item_id, user_id):
    """ Incrementa os votos por item de acordo com as categorias
	Ex.: /api/votes/ID_ITEM/VOTE_TYPE/USER_ID
    """
    if vote_type == 'positive':
        vote = db.items.update({'product_source': int(item_id)}, {"$push": {'evaluated_positive': user_id}})
    if vote_type == 'negative':
        vote = db.items.update({'product_source': int(item_id)}, {"$push": {'evaluated_negative': user_id}})
    if vote_type == 'neutral':
        vote = db.items.update({'product_source': int(item_id)}, {"$push": {'evaluated_neutral': user_id}})
    return "Voted %s %s %s" %(vote_type, item_id, user_id)