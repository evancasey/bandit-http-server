# from flask_peewee.rest import RestAPI, RestResource, UserAuthentication
from flask import request
from app import app, db
import pdb
# from models import User

#---------------------------------------------
# api
# --------------------------------------------

@app.route("/create", methods = ['POST'])
def create():
    ''' create a new bandit '''

    if request.method == "POST":
        data = request.form                
        db.rpush("arms",data['test_key'])
        pdb.set_trace()
        return jsonify(data)