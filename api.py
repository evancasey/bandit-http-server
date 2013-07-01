from flask import request
from app import app, db
from algorithms import epsilon_greedy
import pdb

#---------------------------------------------
# api
# --------------------------------------------

# @app.route("/create", methods = ['POST'])
# def create():
