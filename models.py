import sys
from app import app, init_db

with app.app_context():
	db = init_db()

#---------------------------------------------
# models
# --------------------------------------------

def arm_keys(db):
	return db.hincrby("unique_ids", "arm")

def bandit_keys(db):
	return db.hincrby("unique_ids", "bandit")
