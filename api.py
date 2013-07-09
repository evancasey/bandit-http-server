import os
from flask import request, session, url_for, jsonify, abort, make_response
from app import app, db
from models import arm_keys, bandit_keys
from algorithms import epsilon_greedy
import pdb
import json

#---------------------------------------------
# api routes
# --------------------------------------------

@app.route("/api/v1.0/bandits", methods = ['POST'])
def create_bandit():
	''' Create a new bandit experiment '''

	# if not a json request throw a 400 error
	if not request.json:
		abort(400)

	# if params not given or improper, throw a 401 error
	if not all (p in request.json for p in ('name','arm_count','algo_type','budget_type','budget', 'reward_type')) \
		or (request.json['arm_count'] < 0) \
		or (request.json['algo_type'] not in ('egreedy','softmax')) \
		or (request.json['budget_type'] not in ('trials')) \
		or (request.json['budget'] < 0) \
		or (request.json['reward_type'] not in ('click')):
		abort(401)

	# if algo_type is egreedy and epsilon is improper or not given, throw a 401 error
	if request.json['algo_type'] == 'egreedy' and not request.json['epsilon'] \
		or ((request.json['epsilon'] <= 0.0) or (request.json['epsilon'] > 1.0)):
		abort(401)

	if request.json['reward_type'] in ('click'):
		max_reward = 1

	arms = {}
	for i in range(request.json['arm_count']):
		arms[arm_keys()] = {
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
		'epsilon': request.json.get('epsilon', ""), # egreedy
		'temperature': request.json.get('temperature', ""), # softmax		
		'reward_type': request.json['reward_type'],
		'max_reward': max_reward,
		'total_reward': 0,
		'total_count': 0,
		'regret': 0
	}

	db.hset("bandits", bandit_keys(), json.dumps(bandit))

	return jsonify( { "name" : bandit['name'], "bandit_id" : db.hget("unique_ids", "bandit"), "arm_ids" : bandit['arms'].keys()} ), 201

@app.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['GET'])
def get_bandit(bandit_id):
	''' Lookup a bandit by its ID '''

	try:
		bandit_dict = eval(db.hget("bandits", bandit_id))
	except TypeError:
		abort(404)

	#TODO: Add regret, other stats
	return jsonify( { 'name' : bandit_dict['name'], 'total_reward' : bandit_dict['total_reward'], 'total_count' : bandit_dict['total_count'], 'regret' : bandit_dict['regret'] } )
@app.route("/api/v1.0/bandits/<int:bandit_id>/arms/current", methods = ['GET'])
def get_current_arm(bandit_id):
	''' Get the bandit's "best" arm '''

	try:
		bandit_dict = eval(db.hget("bandits", bandit_id))
	except TypeError:
		abort(404)

	# initialize the bandit algo class object
	bandit = epsilon_greedy.EpsilonGreedy(bandit_dict)

	# find the "best" arm
	current_arm = epsilon_greedy.EpsilonGreedy.select_arm(bandit)

	return jsonify( { 'current_arm' : current_arm } )

@app.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['PUT'])
def update_bandit(bandit_id):
	''' Update a bandit's name, algo_type, budget_type, budget, or epsilon '''

	# if not a json request throw a 400 error
	if not request.json:
		abort(400)

	try:
		bandit_dict = eval(db.hget("bandits", bandit_id))
	except TypeError:
		abort(404)

	# update these fields if provided
	bandit_dict['name'] = request.json.get('name', bandit_dict['name'])
	bandit_dict['algo_type'] = request.json.get('algo_type', bandit_dict['algo_type'])
	bandit_dict['budget_type'] = request.json.get('budget_type', bandit_dict['budget_type'])
	bandit_dict['budget'] = request.json.get('budget', bandit_dict['budget'])
	bandit_dict['epsilon'] = request.json.get('epsilon', bandit_dict['epsilon'])

	db.hset("bandits", bandit_id, bandit_dict)

	# TODO: add some other stuff here
	return jsonify(bandit_dict)

@app.route("/api/v1.0/bandits/<int:bandit_id>/arms/<int:arm_id>", methods = ['PUT'])
def update_arm(bandit_id, arm_id):

	# if not a json request throw a 400 error
	if not request.json:
		abort(400)

	# if params not give throw 401 error
	if not 'reward' in request.json:
		abort(401)

	try:
		bandit_dict = eval(db.hget("bandits", bandit_id))
		arm = bandit_dict['arms'][str(arm_id)]
	except TypeError, KeyError:
		abort(404)

	# initialize the bandit algo class object
	bandit = epsilon_greedy.EpsilonGreedy(bandit_dict)

	# update the arm
	update_data = epsilon_greedy.EpsilonGreedy.update(bandit, arm_id, request.json['reward'])	

	bandit_dict['arms'][str(arm_id)]['count'] = update_data['count']
	bandit_dict['arms'][str(arm_id)]['value'] = update_data['value']
	bandit_dict['regret'] = update_data['regret']
	bandit_dict['total_reward'] = update_data['total_reward']
	bandit_dict['total_count'] = update_data['total_count']

	db.hset("bandits",bandit_id, bandit_dict)

	# TODO: add some other stuff here
	return jsonify( { bandit_id : bandit_dict['arms'] } )

@app.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['DELETE'])
def delete_bandit(bandit_id):		

	try:
		bandit_dict = eval(db.hget("bandits", bandit_id))
	except TypeError:
		abort(404)

	db.hdel("bandits", bandit_id)

	# TODO: add some other stuff here
	return jsonify( { 'result': True } )

#---------------------------------------------
# error handling
# --------------------------------------------

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'Error': 'Not found'} ), 404)

@app.errorhandler(401)
def missing_params(error):
	return make_response(jsonify( { 'Error': 'Missing or improper parameters'} ), 401)