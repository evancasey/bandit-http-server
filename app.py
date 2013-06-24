import os
from flask import Flask, request, redirect, render_template, session, url_for, send_from_directory, jsonify
from redis import Redis
import json
import datetime
import random

#---------------------------------------------
# initialization
# --------------------------------------------

app = Flask(__name__)
app.config.update(
    DEBUG = True,
)

app.config.from_object('config')

try:
    db = Redis(host='localhost', port=6379, db=0)
except:
    print "Cannot connect to redis server.  Exiting..."
    sys.exit(0)



