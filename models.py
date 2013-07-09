from app import db

#---------------------------------------------
# models
# --------------------------------------------

def arm_keys():
	return db.hincrby("unique_ids", "arm")

def bandit_keys():
	return db.hincrby("unique_ids", "bandit")
