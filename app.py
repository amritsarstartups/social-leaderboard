import os
import sys
import json
from flask import Flask, request, abort, jsonify
from flask_cors import cross_origin

import pymongo
from bson.objectid import ObjectId

from mods.utility import resolve_members



app = Flask(__name__)

db_url = os.environ['SBCON_DB']

@app.route('/', methods=['GET'])
@cross_origin()
def index():
    return  "Hello World!"

def save_data(data, collection):
	client = pymongo.MongoClient(db_url)
	db = client.get_default_database()
	coll = db[collection]
	id  = coll.insert_one(data)
	print("Saved")
	client.close()

def newEncoder(o):
    if type(o) == ObjectId:
        return str(o)
    return o.__str__


def get_data(collection):
	client = pymongo.MongoClient(db_url)
	db = client.get_default_database()
	coll = db[collection]
	return json.dumps({"data":list(coll.find())},  default=newEncoder )




@app.route('/api/v1.0/teams/', methods=['POST', 'GET', 'PUT'])
@cross_origin()
def create_team():
	if request.method == "GET":
		return get_data('teams')

	elif request.method =="POST":
		if not request.json and not "data" in request.json: 
			abort(400)
		try:
			res = request.get_json()
			res = res.get('data')
			members_resolved = resolve_members(res.get('members'))
			data = {
				"name": res.get('name'),
				"picture_url" : res.get('picture_url'),
				"members" : members_resolved,
				"desc": res.get('desc')
			}
			save_data(data, "teams")
			return (jsonify({"response":"success"}), 200)
			return "hello world", 200
		except Exception as e:
			print(e)
			return {"error": "Invalid Parameters"}

@app.route('/api/v1.0/leaderboard/<string:team_id>', methods=["GET"])
@cross_origin()
def send_team_stats(team_id):
	if request.method == "GET":
		if len(team_id)>0:
			client = pymongo.MongoClient(db_url)
			db = client.get_default_database()
			coll = db["stats"]
			return json.dumps({"data":list(coll.find({'_id': ObjectId(team_id)}))},  default=newEncoder)	
	else:
		return {"error": "Invalid Parameters"}

@app.route('/api/v1.0/leaderboard/', methods=["GET"])
@cross_origin()
def send_leaderboard():
	try:
		if request.method == "GET":
			data = get_data('stats')
			return data
	except Exception as e:
		return {"error":str(e)}


@app.route('/api/v1.0/teams/<string:team_id>', methods=["GET"])
@cross_origin()
def send_team(team_id):
	if request.method == "GET":
		if len(team_id)>0:
			client = pymongo.MongoClient(db_url)
			db = client.get_default_database()
			coll = db["teams"]
			return json.dumps({"data":list(coll.find({'_id': ObjectId(team_id)}))},  default=newEncoder)	
	else:
		return {"error": "Invalid Parameters"}

	

if __name__ == '__main__':
    app.run()



