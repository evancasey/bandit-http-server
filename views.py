from flask import render_template  # ...etc , redirect, request, url_for

from app import app
# from models import User

#---------------------------------------------
# controller
# --------------------------------------------

@app.route('/')
def homepage():
    return render_template('index.html')

# @app.route('/private/')
# @auth.login_required
# def private_view():
#     # ...
#     user = auth.get_logged_in_user()
#     return render_tempate(...)