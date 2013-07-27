import os, sys
sys.path.insert(0, '../')
from flask import make_response, jsonify, Blueprint

errors = Blueprint('errors', __name__)

@errors.errorhandler(400)
def bad_request(error):
	return make_response(jsonify( { 'Error': 'Bad Request'} ), 400)
	
@errors.errorhandler(401)
def missing_params(error):
	return make_response(jsonify( { 'Error': 'Missing or improper parameters'} ), 401)

@errors.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'Error': 'Not found'} ), 404)

