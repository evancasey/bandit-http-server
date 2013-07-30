from flask import jsonify
from arm import Arm
import sys
sys.path.insert(0, '../')
from database import Database
import pdb

class Bandit(dict):

	def __init__(self, request):

		arms = {}
		for i in range(request.json['arm_count']):			
			arm = Arm()
			arms[arm.id] = arm.__dict__

		self.id = self.bandit_keys()
		self.name = request.json['name']
		self.arm_count = request.json['arm_count']
		self.arms = arms
		self.algo_type = request.json['algo_type']
		self.budget_type = request.json['budget_type']
		self.budget = request.json['budget']
		self.epsilon = request.json['epsilon']
		self.reward_type = request.json['reward_type']
		self.max_reward = 1
		self.total_reward = 0
		self.total_count = 0
		self.regret = 0

		Database().hset("bandits", self.id, self.__dict__)

	def bandit_keys(self):
		return Database().hincrby("unique_ids", "bandit")

	@classmethod
	def get_bandit(self, id):
		return eval(Database().hget("bandits", id)) 

	def set_bandit(self, id):
		Database().hset("bandits", id, json.dumps(self.__dict__))

	@classmethod
	def is_bandit(self,id):
		if Database().hexists("bandits",id):
			return True
		else:
			return False

	def delete_bandit(id):
		Database().hdel("bandits", id)
