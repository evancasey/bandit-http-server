import os
from flask import request, session, url_for, jsonify, abort, make_response
from app import app, db
from models import armKeys, banditKeys
from algorithms import epsilon_greedy
import pdb
import json

#---------------------------------------------
# api
# --------------------------------------------

@app.route("/api/v1.0/bandits", methods = ['POST'])
def createBandit():
	''' Create a new bandit experiment '''

	# if not a json request throw a 400 error
	if not request.json:
		abort(400)

	# if params not given throw a 401 error
	if not all (p in request.json for p in ('name','arm_count','algo_type','budget_type','budget','epsilon')):
		abort(401)

	arms = {}
	for i in range(request.json['arm_count']):
		arms[armKeys()] = {
			'value': 0,
			'count': 0
		}

	bandit = {
		'name': request.json['name'],
		'arm_count': request.json['arm_count'],
		'arms': arms,
		'algo_type': request.json['algo_type'],
		'budget_type': request.json['budget_type'],
		'budget': request.json['budget'],
		'epsilon': request.json['epsilon']
	}

	db.hset("bandits", banditKeys(), json.dumps(bandit))

	return jsonify( { "name" : bandit['name'], "bandit_id" : db.hget("unique_ids", "bandit"), "arm_ids" : arm_keys_arr} ), 201


@app.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['GET'])
def getBandit(bandit_id):
	''' Lookup a bandit by its ID '''

	try:
		bandit = eval(db.hget("bandits", bandit_id))
	except TypeError:
		abort(404)

	#TODO: Add regret, other stats
	return jsonify(bandit)


@app.route("/api/v1.0/bandits/<int:bandit_id>/arms/current", methods = ['GET'])
def getCurrentArm(bandit_id):
	''' Get the bandit's "best" arm '''

	try:
		bandit = eval(db.hget("bandits", bandit_id))
	except TypeError:
		abort(404)

	return jsonify( { 'current_arm' : epsilon_greedy.selectArm(bandit) } )


@app.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['PUT'])
def updateBandit(bandit_id):
	''' Update a bandit's name, algo_type, budget_type, budget, or epsilon '''

	# if not a json request throw a 400 error
	if not request.json:
		abort(400)

	try:
		bandit = eval(db.hget("bandits", bandit_id))
	except TypeError:
		abort(404)

	# update these fields if provided
	bandit['name'] = request.json.get('name', bandit['name'])
	bandit['algo_type'] = request.json.get('algo_type', bandit['algo_type'])
	bandit['budget_type'] = request.json.get('budget_type', bandit['budget_type'])
	bandit['budget'] = request.json.get('budget', bandit['budget'])
	bandit['epsilon'] = request.json.get('epsilon', bandit['epsilon'])

	db.hset("bandits", bandit_id, bandit)

	# TODO: add some other stuff here
	return jsonify(bandit)


@app.route("/api/v1.0/bandits/<int:bandit_id>/arms/<int:arm_id>", methods = ['PUT'])
def updateArm(bandit_id, arm_id):

	bandit = db.hget("bandits", bandit_id)

	# if bad bandit ID, throw 404 error
	if bandit == None:
		abort(404)

	# if not a json request throw a 400 error
	if not request.json:
		abort(400)

	# convert to dict 
	bandit_dict = json.loads(json.dumps(bandit))

	pdb.set_trace()

	# if bad arm ID, throw 404 error
	if bandit_dict['arms'] == None:
		abort(404)

	# if params not give throw 401 error
	if not 'reward' in request.json:
		abort(401)

	reward = request.json['reward']

	bandit_dict = epsilon_greedy.update(bandit_dict, arm_id, reward)

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