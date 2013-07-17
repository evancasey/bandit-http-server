import os
import sys
from flask import Flask, g
from redis import Redis
import pdb

#---------------------------------------------
# initialization
# --------------------------------------------

app = Flask(__name__)
app.config.update(
    DEBUG = True,
)

def init_db(*args, **kwargs):
	app = kwargs["app"]
	if kwargs.get("test", False) == True or app.config['TESTING']:
		try:
			return Redis(host='localhost', port=6379, db=1)						
		except:
			print "Cannot connect to redis test server.  Exiting..."
			sys.exit(0)
	else:
		try:	
			print "DEV"
			return Redis(host='localhost', port=6379, db=0)
		except:
			print "Cannot connect to redis test server.  Exiting..."
			sys.exit(0)

def get_db(*args, **kwargs):
	app = kwargs["app"]
	with app.app_context():
		db = getattr(g, 'db', None)
		if db is None:
			if kwargs.get("test", False) == True:
				db = init_db(app = app, test = True)
			else:
				db = init_db(app = app)
		return db

