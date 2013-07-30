from redis import Redis
import sys	
import pdb

class Database(object):
	__db = None

	def __new__(cls, **kwargs):
		
		if cls.__db is None:
			try:								
				cls.__db = Redis(host='localhost', port=6379, db=kwargs['app'].config['REDIS_DB'])
			except:
				print "Cannot connect to redis test server.  Exiting..."
				sys.exit(0)
		
		return cls.__db

def get_test_db():
	return Redis(host='localhost', port=6379, db=1)