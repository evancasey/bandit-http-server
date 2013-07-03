import os
from flask import request, session, url_for, jsonify, abort, make_response
from app import app, db
import helper
import pdb

#---------------------------------------------
# api
# --------------------------------------------

# Create a new bandit
@app.route("/api/v1.0/bandits", methods = ['POST'])
def createBandit():

	if not request.json:
		abort(400)

	# Initialize the arms
	arms = {}
	for i in range(request.json['arm_count']):
		arms[helper.armKeys()] = {
			'value': 0
		}
	
	# Initialize the bandit
	bandit = {
		'arm_count': request.json['arm_count'],
		'arms': arms,
		'algo_type': request.json['algo_type'],
		'horizon_type': request.json['horizon_type'],
		'horizon_value': request.json['horizon_value'],
		'epsilon': request.json['epsilon']
	}

	db.hset("bandits", helper.banditKeys(), bandit)

	#TODO: change this
	return jsonify( { db.hget("unique_ids", "bandit"): bandit} ), 201


# Look up by bandit ID
@app.route("/api/v1.0/bandits/<int:bandit_id>", methods = ['GET'])
def getBandit(bandit_id):
	bandit = db.hget("bandits", bandit_id)
	if len(bandit) == 0:
		abort(404)
	return jsonify( {'bandit': bandit} )

# #TODO: add this
# @app.route("/api/v1.0/bandits/<int:bandit_id>"), methods = ['PUT'])
# def updateBandit():

# #TODO: add this
# @app.route("/api/v1.0/bandits/<int:bandit_id>"), mothads = ['DELETE'])
# def deleteBandit():


# Error handling
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'Error': 'Not found'} ), 404)