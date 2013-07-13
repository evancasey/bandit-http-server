import os	
import sys
import pdb
import unittest
import tempfile
import time
import subprocess
import signal

sys.path.insert(0, '../')
from app import app, init_db

sys.path.insert(0, '../client/')
from client import BanditClient

class BanditUnitTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):

		# run main.py will args = "--test",
		cmd = "python ../main.py --test"
		self.p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)		
		time.sleep(3)		

		# set the python wrapper to client
		self.client = BanditClient()

		# clear the db
		init_db().flushdb()

	@classmethod
	def tearDownClass(self):	
		# kill the process	
		os.killpg(self.p.pid, signal.SIGTERM)

class BanditClientTests(BanditUnitTest):
	

	def setUp(self):
		rv = self.client.bandit_create(name = "my experiment", arm_count=4)	

	def test_bandit_create(self):

		# test create works with good params
		rv = self.client.bandit_create(name = "success", arm_count=4)		
		assert isinstance(rv, dict)
		assert rv['name'] == "created test"
		print rv	

		# test create fails with bad params
		rv = self.client.bandit_create(name = "fail")
		assert 'HTTPError: 401' in rv

	def test_bandit_get(self):

		# test get bandit works with good params
		rv = self.client.bandit_get(1)
		assert isinstance(rv, dict)
		assert rv['name'] == "my experiment"

		# test get band
		pass

	@classmethod
	def tearDown(self):
		init_db().flushdb()


if __name__ == '__main__':
	unittest.main() 