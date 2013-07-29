import os
import sys
from flask import Flask, g
import pdb

def config_str_to_obj(cfg):
	if isinstance(cfg, basestring):
		module = __import__('config', fromlist=[cfg])
		return getattr(module, cfg)
	return cfg

def start_app(config):
	app = Flask(__name__)
	pdb.set_trace()

	config = config_str_to_obj(config)
	configure_app(app, config) # apply the config env to app
	configure_blueprints(app)
	configure_database(app) 
	# ...insert other configs here
	return app

def configure_app(app,config):
	app.config.from_object(config)
	app.config.from_envvar("APP_CONFIG", silent=True)

def configure_blueprints(app):
	from api import api
	from lib import errors
	app.register_blueprint(api)
	app.register_blueprint(errors)

def configure_database(app):
	from database import Database
	Database(app=app)

