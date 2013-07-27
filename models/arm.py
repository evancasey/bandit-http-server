import sys
import pdb
import inspect
sys.path.insert(0, '../')
from database import Database

class Arm():

	def __init__(self):
		self.id = self.arm_keys()
		self.count = 0
		self.value = 0

	def arm_keys(self):		
		return Database().hincrby("unique_ids", "arm")

	def get_arm(arm_id, bandit):
		return bandit['arms'][str(arm_id)]	
