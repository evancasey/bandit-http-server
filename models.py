from app import db

#---------------------------------------------
# models
# --------------------------------------------

def armKeys():
	db.hincrby("unique_ids", "arm")
	return db.hget("unique_ids", "arm")

def banditKeys():
	db.hincrby("unique_ids", "bandit")
	return db.hget("unique_ids", "bandit")
