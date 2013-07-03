import os
from flask import request, session, url_for, jsonify, abort, make_response
from app import app, db
from models import armKeys, banditKeys
import pdb
import json
import ast

#---------------------------------------------
# api
# --------------------------------------------

# create a new bandit
@app.route("/api/v1.0/bandits", methods = ['POST'])
def createBandit():

	# if not a json request throw a 400 error
	if not request.json:
		abort(400)

	# if params not given throw a 401 error
	if not ['name','arm_count','algo_type','horizon_type','horizon_value','epsilon'] in request.json:
		abort(401)

	arms = {}
	arm_keys_arr = []
	for i in range(request.json['arm_count']):
		arm_keys_arr.append(armKeys())
		arms[arm_keys_arr[i]] = {
			'value': 0
		}

	bandit = {
		'name': request.json['name'],
		'arm_count': request.json['arm_count'],
		'arms': arms,
		'algo_type': request.json['algo_type'],
		'horizon_type': request.json['horizon_type'],
		'horizon_value': request.json['horizon_value'],
		'epsilon': request.json['epsilon']
	}

	db.hset("bandits", banditKeys(), bandit)

	return jsonify( { "name" : bandit['name'], "bandit_id" : db.hget("unique_ids", "bandit"), "arm_ids" : arm_keys_arr} ), 201


# look up by bandit ID
@app.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['GET'])
def getBandit(bandit_id):

	bandit = ast.literal_eval(db.hget("bandits", bandit_id))

	# if bad ID, throw 404 error
	if len(bandit) == 0:
		abort(404)

	# TODO: add some other stuff here
	return jsonify( {'name': bandit['name'], 'arms': bandit['arms']} )


# update an existing bandit
@app.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['PUT'])
def updateBandit(bandit_id):

	bandit = ast.literal_eval(db.hget("bandits", bandit_id))

	# if bad ID, throw 404 error
	if len(bandit) == 0:
		abort(404)

	# if not a json request throw a 400 error
	if not request.json:
		abort(404)

	bandit['name'] = request.json.get('name', bandit['name'])
	bandit['arm_count'] = request.json.get('arm_count', bandit['arm_count'])
	bandit['algo_type'] = request.json.get('algo_type', bandit['algo_type'])
	bandit['horizon_type'] = request.json.get('horizon_type', bandit['horizon_type'])
	bandit['horizon_value'] = request.json.get('horizon_value', bandit['horizon_value'])
	bandit['epsilon'] = request.json.get('epsilon', bandit['epsilon'])

	# TODO: add some other stuff here
	return jsonify( { bandit_id : bandit } )


# delete an existing bandit
@app.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['DELETE'])
def deleteBandit(bandit_id):
	
	bandit = db.hget("bandits", bandit_id)

	# if bad ID, throw 404 error
	if len(bandit) == 0:
		abort(404)

	db.hdel("bandits", bandit_id)

	return jsonify( { 'result': True } )


# error handling
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'Error': 'Not found'} ), 404)

# error handling
@app.errorhandler(401)
def missing_params(error):
	return make_response(jsonify( { 'Error': 'Missing parameters'} ), 401)