from flask import abort
import pdb

def json_request(request):

	# request data must be formatted in json
	if not request.json:
		abort(400)

def create_params(request):
	
	# name, arm_count, algo_type, budget_type, budget, reward_type, and epsilon must be given
	if not all (p in request.json for p in ('name','arm_count','algo_type','budget_type','budget', 'reward_type', 'epsilon')) \
		or (request.json['arm_count'] < 0) \
		or (request.json['algo_type'] not in ('egreedy','softmax')) \
		or (request.json['budget_type'] not in ('trials')) \
		or (request.json['budget'] < 0) \
		or (request.json['reward_type'] not in ('click')) \
		or (request.json['epsilon'] <= 0.0):
		abort(401)

def bandit_exists(bandit_id, db):

	# bandit id must exist as a key
	if db.hexists("bandits", bandit_id):
		return True
	else:
		abort(404)

def arm_exists(arm_id, dict):

	# arm id must exist as a key
	if dict['arms'].has_key(str(arm_id)):
		return True
	else:
		abort(404)

def update_arm_params(request):
	# reward param must be present
	if not 'reward' in request.json:
		abort(401)