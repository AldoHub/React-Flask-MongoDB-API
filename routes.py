from flask import Blueprint, request, jsonify
import json
import pymongo
from dotenv import load_dotenv
import os
import sys
from pymongo import MongoClient
from bson import ObjectId

#JSONEncoder to manage the MongoDB ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


#load env file
load_dotenv()

#------ MongoDB
connection = "<mongodb_url>"
client = MongoClient(connection)
db = client["nodestripe"]
collection = db["items"]

#------ Blueprint definitions
indexRoute = Blueprint("index", __name__)
createRoute = Blueprint("create", __name__)
itemRoute = Blueprint("item", __name__)
updateRoute = Blueprint("update", __name__)
deleteRoute = Blueprint("delete", __name__)


#----- routes
#all items route
@indexRoute.route("/api/items")
def index():

    items = []
    #get all items from the collection
    cursor = collection.find({})
    #loop to get the needed data
    for document in cursor:
       #we need to encode the MongoDBId here
       items.append({"_id": JSONEncoder().encode(document["_id"]),"name": document["name"], "image": document["image"]})
    #return the items
    return jsonify(data= items)


#single item route
@itemRoute.route("/api/item/<id>", methods=["GET"])
def item(id):
    cursor = collection.find_one({"_id": ObjectId(id)})
    print(cursor, flush=True)
    
    #return the encoded item
    return jsonify(data=JSONEncoder().encode(cursor))



#create new item route
@createRoute.route("/api/create", methods=["POST"])
def create():
    print(request.json, flush=True)

    name = request.json.get("name")
    description = request.json.get("description")
    image = request.json.get("image")
    amount = request.json.get("amount")


    item = {
        "name": name,
        "description": description,
        "image": image,
        "amount": amount
    }

    collection.insert_one(item)
    return jsonify(data="item created successfully")


#update item
@updateRoute.route("/api/update/<id>", methods=["PUT"])
def update(id):
    print(request.json, flush=True)
    
    itemid= request.json.get("itemid")
    name = request.json.get("name")
    description = request.json.get("description")
    image = request.json.get("image")
    amount = request.json.get("amount")


    updatedItem = {
        "name": name,
        "description": description,
        "image": image,
        "amount": amount
    }

    collection.update_one({"_id": ObjectId(itemid)}, {"$set": updatedItem})
    return jsonify(data = "update response")    


@deleteRoute.route("/api/delete/<id>", methods = ["DELETE"])
def delete(id):
    print(request.json, flush=True)
    itemid = request.json.get("id")
    collection.remove({"_id": ObjectId(itemid)})

    return jsonify(data= "ited delete successfully")    