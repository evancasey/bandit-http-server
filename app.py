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

def init_db():
	if app.config['TESTING'] == True:
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
