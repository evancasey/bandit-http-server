import os
import sys
import pdb
import json

from flask import request, session, url_for, jsonify, make_response, _app_ctx_stack, g
from app import app, get_db
from models import arm_keys, bandit_keys
from algorithms import epsilon_greedy, softmax
from lib import validations


@app.before_request
def before_request():
	''' Initialize the redis db before each request '''

	g.db = get_db(app = app)


@app.route("/api/v1.0/bandits", methods = ['POST'])
def create_bandit():
	''' Create a new bandit experiment '''

	# if not a json request throw a 400 error
	validations.json_request(request)

	# if params not given or improper, throw a 401 error
	validations.create_params(request)

	if request.json['reward_type'] in ('click'):
		max_reward = 1

	arms = {}
	for i in range(request.json['arm_count']):
		arms[arm_keys(g.db)] = {
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
		'reward_type': request.json['reward_type'],
		'max_reward': max_reward,
		'total_reward': 0,
		'total_count': 0,
		'regret': 0
	}

	bandit_id = bandit_keys(g.db)
	g.db.hset("bandits", bandit_id, json.dumps(bandit))

	return jsonify( {"bandit_id" : int(bandit_id), "name" : bandit['name'], "arm_ids" : bandit['arms'].keys()} ), 201


@app.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['GET'])
def get_bandit(bandit_id):
	''' Lookup a bandit by its ID '''

	# if bandit exists, find it
	if validations.bandit_exists(bandit_id, g.db):
		bandit_dict = eval(g.db.hget("bandits", bandit_id)) 

	return jsonify( { "bandit_id" : bandit_id, 'name' : bandit_dict['name'], 'total_reward' : bandit_dict['total_reward'], \
		'total_count' : bandit_dict['total_count'], 'regret' : bandit_dict['regret']} )


@app.route("/api/v1.0/bandits/<int:bandit_id>/arms/current", methods = ['GET'])
def get_current_arm(bandit_id):
	''' Get the bandit's "best" arm '''

	# if bandit exists, find it
	if validations.bandit_exists(bandit_id, g.db):
		bandit_dict = eval(g.db.hget("bandits", bandit_id)) 

	# initialize the bandit class object
	bandit = _set_bandit(bandit_dict)

	# find the "best" arm
	current_arm = bandit.select_arm()

	return jsonify( { 'bandit_id' : bandit_id, 'current_arm' : current_arm } )


@app.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['PUT'])
def update_bandit(bandit_id):
	''' Update a bandit's name, algo_type, budget_type, budget, epsilon, reward_type, or max_reward '''

	# if not a json request throw a 400 error
	validations.json_request(request)

	# if bandit exists, find it
	if validations.bandit_exists(bandit_id, g.db):
		bandit_dict = eval(g.db.hget("bandits", bandit_id)) 

	# update these fields if provided
	bandit_dict['name'] = request.json.get('name', bandit_dict['name'])
	bandit_dict['algo_type'] = request.json.get('algo_type', bandit_dict['algo_type'])
	bandit_dict['budget_type'] = request.json.get('budget_type', bandit_dict['budget_type'])
	bandit_dict['budget'] = request.json.get('budget', bandit_dict['budget'])
	bandit_dict['epsilon'] = request.json.get('epsilon', bandit_dict['epsilon'])
	bandit_dict['reward_type'] = request.json.get('reward_type', bandit_dict['reward_type'])
	bandit_dict['max_reward'] = request.json.get('max_reward', bandit_dict['max_reward'])

	g.db.hset("bandits", bandit_id, bandit_dict)

	# TODO: add some other stuff here
	return jsonify( {"bandit_id" : bandit_id, "name" : bandit_dict['name'], "algo_type" : bandit_dict['algo_type'], \
		"budget_type" : bandit_dict['budget_type'], "budget" : bandit_dict["budget"], "epsilon" : bandit_dict["epsilon"], \
		"reward_type" : bandit_dict["reward_type"], "max_reward" : bandit_dict["max_reward"]} )


@app.route("/api/v1.0/bandits/<int:bandit_id>/arms/<int:arm_id>", methods = ['PUT'])
def update_arm(bandit_id, arm_id):

	# if not a json request throw a 400 error
	validations.json_request(request)

	# if params not give throw 401 error
	validations.update_arm_params(request)

	if validations.bandit_exists(bandit_id, g.db):
		bandit_dict = eval(g.db.hget("bandits", bandit_id)) 
		if validations.arm_exists(arm_id, bandit_dict):
			arm = bandit_dict['arms'][str(arm_id)]	

	# initialize the bandit algo class object
	bandit = _set_bandit(bandit_dict)

	# call an algo to update an arm
	bandit.update(str(arm_id), request.json['reward'])	

	# update the bandit's arm with the values update returns
	bandit_dict['arms'][str(arm_id)]['count'] = bandit.counts[str(arm_id)]
	bandit_dict['arms'][str(arm_id)]['value'] = bandit.values[str(arm_id)]
	bandit_dict['regret'] = bandit.regret
	bandit_dict['total_reward'] = bandit.total_reward
	bandit_dict['total_count'] = bandit.total_count

	g.db.hset("bandits", bandit_id, bandit_dict)

	# TODO: add some other stuff here
	return jsonify( { "bandit_id" : bandit_id, "regret" : bandit_dict['regret'], "total_reward" : bandit_dict["total_reward"], \
		"total_count" : bandit_dict['total_count'], "arms": bandit_dict['arms'] } )


@app.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['DELETE'])
def delete_bandit(bandit_id):		

	# if bandit exists, find it
	if validations.bandit_exists(bandit_id, g.db):
		bandit_dict = eval(g.db.hget("bandits", bandit_id)) 
	g.db.hdel("bandits", bandit_id)

	# TODO: add some other stuff here
	return jsonify( { 'result': True } )


#---------------------------------------------
# bandit class methods
# --------------------------------------------

def _set_bandit(bandit):
	# helper method to initialize the correct bandit class object
	return {
		'egreedy' : epsilon_greedy.EpsilonGreedy(bandit),
		'softmax' : softmax.Softmax(bandit)
	}[bandit['algo_type']]