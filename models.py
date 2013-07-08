from app import db

#---------------------------------------------
# models
# --------------------------------------------

def armKeys():
	return db.hincrby("unique_ids", "arm")

def banditKeys():
	return db.hincrby("unique_ids", "bandit")
