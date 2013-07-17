import sys

#---------------------------------------------
# models
# --------------------------------------------

def arm_keys(db):
	return db.hincrby("unique_ids", "arm")

def bandit_keys(db):
	return db.hincrby("unique_ids", "bandit")
