import os
import sys
import pdb
from redis import Redis
import unittest
import tempfile
from client import BanditClient

class BanditClientTestCase(unittest.TestCase):

	def setUp(self):		
		try:
			# set up the test db
		    self.db = Redis(host='localhost', port=6380, db=0)
		except:
		    print "Cannot connect to redis server.  Exiting..."
		    sys.exit(0)

		self.client = BanditClient()


	def test_bandit_create(self):

		# test create works with good params
		rv = self.client.bandit_create(name = "my experiment", arm_count=4)
		assert 'HTTPError: 404' not in rv
		assert 'HTTPError: 401' not in rv

		# test create fails with bad params
		rv = self.client.bandit_create(name = "my experiment")
		assert 'HTTPError: 401' in rv


if __name__ == '__main__':
	unittest.main() 