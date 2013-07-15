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
	if app.config['TESTING'] or kwargs.get('type', None) == "test":
		try:
			return Redis(host='localhost', port=6379, db=1)						
		except:
			print "Cannot connect to redis test server.  Exiting..."
			sys.exit(0)
	else:
		try:		
			return Redis(host='localhost', port=6379, db=0)
		except:
			print "Cannot connect to redis test server.  Exiting..."
			sys.exit(0)

def get_db(*args, **kwargs):
	with kwargs["app"].app_context():
		db = getattr(g, 'db', None)
		if db is None:
			db = init_db(type = kwargs["type"])
		return db

