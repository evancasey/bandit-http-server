import os
import sys
import pdb
import json

from flask import request, session, url_for, jsonify, make_response, _app_ctx_stack, Blueprint
from models.arm import Arm
from models.bandit import Bandit
from algorithms import epsilon_greedy, softmax
from lib import validations

api = Blueprint('api', __name__)


@api.route("/api/v1.0/bandits", methods = ['POST'])
def create_bandit():
	''' Create a new bandit experiment '''

	# if not a json request throw a 400 error
	validations.json_request(request)

	# if params not given or improper, throw a 401 error
	validations.create_params(request)

	# initialize and store the bandit in redis
	bandit = Bandit(request)

	return jsonify( {"bandit_id" : bandit.id, "name" : bandit.name, "arm_ids" : bandit.arms.keys()} ), 201


@api.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['GET'])
def get_bandit(bandit_id):
	''' Lookup a bandit by its ID '''

	# if bandit exists, find it
	if validations.bandit_exists(bandit_id):
		bandit_dict = Bandit.get_bandit(bandit_id)

	return jsonify( { "bandit_id" : bandit_id, 'name' : bandit_dict['name'], 'total_reward' : bandit_dict['total_reward'], \
		'total_count' : bandit_dict['total_count'], 'regret' : bandit_dict['regret']} )


@api.route("/api/v1.0/bandits/<int:bandit_id>/arms/current", methods = ['GET'])
def get_current_arm(bandit_id):
	''' Get the bandit's "best" arm '''

	# if bandit exists, find it
	if validations.bandit_exists(bandit_id):
		bandit_dict = Bandit.get_bandit(bandit_id)

	# initialize the bandit class object and find the "best" arm
	current_arm = _start_algo(bandit_dict).select_arm()

	return jsonify( { 'bandit_id' : bandit_id, 'current_arm' : current_arm } )


@api.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['PUT'])
def update_bandit(bandit_id):
	''' Update a bandit's name, algo_type, budget_type, budget, epsilon, reward_type, or max_reward '''

	# if not a json request throw a 400 error
	validations.json_request(request)

	# if bandit exists, find it
	if validations.bandit_exists(bandit_id):
		bandit_dict = Bandit.get_bandit(bandit_id)

	# update these fields if provided
	bandit_dict['name'] = request.json.get('name', bandit_dict['name'])
	bandit_dict['algo_type'] = request.json.get('algo_type', bandit_dict['algo_type'])
	bandit_dict['budget_type'] = request.json.get('budget_type', bandit_dict['budget_type'])
	bandit_dict['budget'] = request.json.get('budget', bandit_dict['budget'])
	bandit_dict['epsilon'] = request.json.get('epsilon', bandit_dict['epsilon'])
	bandit_dict['reward_type'] = request.json.get('reward_type', bandit_dict['reward_type'])
	bandit_dict['max_reward'] = request.json.get('max_reward', bandit_dict['max_reward'])

	bandit.set_bandit(bandit_id, bandit)

	# TODO: add some other stuff here
	return jsonify( {"bandit_id" : bandit_id, "name" : bandit_dict['name'], "algo_type" : bandit_dict['algo_type'], \
		"budget_type" : bandit_dict['budget_type'], "budget" : bandit_dict["budget"], "epsilon" : bandit_dict["epsilon"], \
		"reward_type" : bandit_dict["reward_type"], "max_reward" : bandit_dict["max_reward"]} )


@api.route("/api/v1.0/bandits/<int:bandit_id>/arms/<int:arm_id>", methods = ['PUT'])
def update_arm(bandit_id, arm_id):

	# if not a json request throw a 400 error
	validations.json_request(request)

	# if params not give throw 401 error
	validations.update_arm_params(request)

	if validations.bandit_exists(bandit_id):
		bandit_dict = Bandit.get_bandit(bandit_id)
		if validations.arm_exists(arm_id, bandit_dict):
			arm = arm.get_arm(arm_id, bandit_dict)

	# initialize the bandit algo class object and call update 
	bandit = _start_algo(bandit_dict).update(str(arm_id), request.json['reward'])	

	# update the bandit's arm with the values update returns
	bandit_dict['arms'][str(arm_id)]['count'] = bandit.counts[str(arm_id)]
	bandit_dict['arms'][str(arm_id)]['value'] = bandit.values[str(arm_id)]
	bandit_dict['regret'] = bandit.regret
	bandit_dict['total_reward'] = bandit.total_reward
	bandit_dict['total_count'] = bandit.total_count

	bandit.set_bandit(bandit_id, bandit_dict)

	# TODO: add some other stuff here
	return jsonify( { "bandit_id" : bandit_id, "regret" : bandit_dict['regret'], "total_reward" : bandit_dict["total_reward"], \
		"total_count" : bandit_dict['total_count'], "arms": bandit_dict['arms'] } )


@api.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['DELETE'])
def delete_bandit(bandit_id):		

	# if bandit exists, find it
	if validations.bandit_exists(bandit_id):
		bandit_dict = Bandit.get_bandit(bandit_id)

	bandit.delete_bandit(bandit_id)

	# TODO: add some other stuff here
	return jsonify( { 'result': True } )


#---------------------------------------------
# algo class methods
# --------------------------------------------

def _start_algo(bandit):
	# helper method to initialize the correct bandit class object
	return {
		'egreedy' : epsilon_greedy.EpsilonGreedy(bandit),
		'softmax' : softmax.Softmax(bandit)
	}[bandit['algo_type']]