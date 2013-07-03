import os
from flask import request, session, url_for, jsonify, abort, make_response
from app import app, db
from models import armKeys, banditKeys
from algorithms.epsilon_greedy import selectArm, update
import pdb
import json
import ast

#---------------------------------------------
# api
# --------------------------------------------

@app.route("/api/v1.0/bandits", methods = ['POST'])
def createBandit():

	# if not a json request throw a 400 error
	if not request.json:
		abort(400)

	# if params not given throw a 401 error
	if not all (p in request.json for p in ('name','arm_count','algo_type','horizon_type','horizon_value','epsilon')):
		abort(401)

	arms = {}
	arm_keys_arr = []

	for i in range(request.json['arm_count']):
		arm_keys_arr.append(armKeys())
		arms[arm_keys_arr[i]] = {
			'value': 0,
			'count': 0
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


@app.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['GET'])
def getBandit(bandit_id):

	bandit = db.hget("bandits", bandit_id)

	# if bad bandit ID, throw 404 error
	if bandit == None:
		abort(404)

	# convert to dict 
	bandit_dict = ast.literal_eval(bandit)	

	# TODO: add some other stuff here
	return jsonify( {'name' : bandit_dict['name'], 'arms': bandit_dict['arms'], 'current_arm' : selectArm(bandit_dict)} )


@app.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['PUT'])
def updateBandit(bandit_id):

	bandit = db.hget("bandits", bandit_id)

	# if bad bandit ID, throw 404 error
	if bandit == None:
		abort(404)

	# if not a json request throw a 400 error
	if not request.json:
		abort(400)

	# convert to dict 
	bandit_dict = ast.literal_eval(bandit)

	bandit_dict['name'] = request.json.get('name', bandit_dict['name'])
	bandit_dict['algo_type'] = request.json.get('algo_type', bandit_dict['algo_type'])
	bandit_dict['horizon_type'] = request.json.get('horizon_type', bandit_dict['horizon_type'])
	bandit_dict['horizon_value'] = request.json.get('horizon_value', bandit_dict['horizon_value'])
	bandit_dict['epsilon'] = request.json.get('epsilon', bandit_dict['epsilon'])

	db.hset("bandits", bandit_id, bandit_dict)

	# TODO: add some other stuff here
	return jsonify( { bandit_id : bandit_dict } )


@app.route("/api/v1.0/bandits/<int:bandit_id>/arms/<int:arm_id>", methods = ['PUT'])
def updateArm(bandit_id,arm_id):

	bandit = db.hget("bandits", bandit_id)

	# if bad bandit ID, throw 404 error
	if bandit == None:
		abort(404)

	# if not a json request throw a 400 error
	if not request.json:
		abort(400)

	# convert to dict 
	bandit_dict = ast.literal_eval(bandit)

	# if bad arm ID, throw 404 error
	if bandit_dict['arms'] == None:
		abort(404)

	# if params not give throw 401 error
	if not 'value' in request.json:
		abort(401)

	# reward = bandit_dict['arms'][str(arm_id)]['reward']

	db.hset("bandits", bandit_id, bandit_dict)

	# TODO: add some other stuff here
	return jsonify( { bandit_id : bandit_dict['arms'] } )



@app.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['DELETE'])
def deleteBandit(bandit_id):
	
	bandit = db.hget("bandits", bandit_id)

	# if bad bandit ID, throw 404 error
	if bandit == None:
		abort(404)

	db.hdel("bandits", bandit_id)

	# TODO: add some other stuff here
	return jsonify( { 'result': True } )


# error handling
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'Error': 'Not found'} ), 404)


# error handling
@app.errorhandler(401)
def missing_params(error):
	return make_response(jsonify( { 'Error': 'Missing parameters'} ), 401)