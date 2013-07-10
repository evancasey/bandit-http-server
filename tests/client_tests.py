import os
import imp
import sys
import pdb
import unittest
import tempfile
from app import db

sys.path.insert(0, '../client/')
from client import BanditClient


class BanditClientTestCase(unittest.TestCase):

	# runs before every
	def setUp(self):		
		self.db = db
		self.client = BanditClient()		
		self.db.flushdb() #clear the db

	def test_bandit_create(self):

		# test create works with good params
		rv = self.client.bandit_create(name = "my experiment", arm_count=4)		
		assert isinstance(rv, dict)
		assert rv['name'] == "my experiment"
		print rv	

		# test create fails with bad params
		rv = self.client.bandit_create(name = "my experiment")
		assert 'HTTPError: 401' in rv

	def test_bandit_get(self):

		# test get bandit works with good params
		# rv = self.client.bandit_get(1)
		# assert isinstance(rv, dict)
		# assert rv['name'] == "my experiment"

		# test get band
		pass

	def tearDown(self):
		pass


if __name__ == '__main__':
	unittest.main() 