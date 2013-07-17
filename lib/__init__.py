import os, sys
sys.path.insert(0, '../')
from flask import make_response, jsonify
from app import app

@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify( { 'Error': 'Bad Request'} ), 400)
	
@app.errorhandler(401)
def missing_params(error):
	return make_response(jsonify( { 'Error': 'Missing or improper parameters'} ), 401)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'Error': 'Not found'} ), 404)

