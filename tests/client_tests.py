import os	
import sys
import pdb
import unittest
import tempfile
import time
import subprocess
import signal

sys.path.insert(0, '../')
from app import app, get_db

sys.path.insert(0, '../client/')
from client import BanditClient

class BanditUnitTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
	
		# run main.py with args: --test, and wait for it to terminate
		cmd = ["python", "../main.py", "--test"]
		self.p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
		time.sleep(2)		

		# if not running, check for errors
		if self.p.poll() != None:
			output, errors = self.p.communicate()
			if self.p.returncode:
				print self.p.returncode
				sys.exit(errors)
			else:
				print output	

		# set the python wrapper to client
		self.client = BanditClient()

		# connect to the test db
		self.db = get_db(app = app, test = True)
		self.db.flushdb()

	@classmethod
	def tearDownClass(self):	
		# kill the process	
		os.killpg(self.p.pid, signal.SIGTERM)

class BanditClientTests(BanditUnitTest):
	
	def setUp(self):
		rv = self.client.bandit_create(name = "my_experiment", arm_count=4)	

	def test_create_bandit(self):

		self.db.flushdb()

		# test create works with good params
		bandit_id = 1
		rv = self.client.bandit_create(name = "success", arm_count=4)	
		assert rv['bandit_id'] == bandit_id

		# test create fails with bad params
		rv = self.client.bandit_create(name = "failure") 
		assert 'HTTPError: 401' in rv

	def test_get_bandit(self):

		# test get bandit works with good id
		bandit_id = 1
		rv = self.client.bandit_get(bandit_id)
		assert rv['bandit_id'] == bandit_id

		# test get bandit fails with bad id
		rv = self.client.bandit_get(2)
		assert 'HTTPError: 404' in rv

	def test_get_current_arm(self):

		# test get current arm works with good id
		bandit_id = 1
		rv = self.client.arm_get_current(bandit_id)
		assert rv['bandit_id'] == bandit_id

		# test get current arm fails with bad id
		rv = self.client.arm_get_current(2)
		assert 'HTTPError: 404' in rv

	# def test_get_arm(self):

	# 	# test get arm works with good id
	# 	bandit_id = 1
	# 	arm_id = 1
	# 	rv = self.client.arm_get(bandit_id, arm_id)
	# 	assert rv['bandit_id'] == bandit_id
	# 	assert rv['arm_id'] == arm_id

	# 	# test get current arm fails with bad params
	# 	rv = self.client.arm_get(2)
	# 	assert 'HTTPError: 404' in rv

	def test_update_bandit(self):

		# test update bandit works with good id
		bandit_id = 1
		rv = self.client.bandit_update(bandit_id = bandit_id, name = "updated_name")
		assert rv['name'] == "updated_name"

		# test update bandit fails with bad id
		rv = self.client.bandit_update(bandit_id = 2, name = "updated_name")
		assert 'HTTPError: 404' in rv

	def test_update_arm(self):

		# test update arm works with good id and good params
		bandit_id = 1
		arm_id = 1
		rv = self.client.arm_update(bandit_id = bandit_id, arm_id = arm_id, reward = 1)
		assert rv['total_reward'] == 1

		# test update arm fails with bad bandit id
		rv = self.client.arm_update(bandit_id = 2, arm_id = arm_id, reward = 1)
		assert 'HTTPError: 404' in rv

		# test update arm fails with bad arm id
		rv = self.client.arm_update(bandit_id = bandit_id, arm_id = 5, reward = 1)
		assert 'HTTPError: 404' in rv

		# test update arm fails with bad params
		rv = self.client.arm_update(bandit_id = bandit_id, arm_id = arm_id)
		assert 'HTTPError: 400' in rv

	def tearDown(self):
		# clear the db
		self.db.flushdb()


if __name__ == '__main__':
	unittest.main() 