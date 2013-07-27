#TODO: Add dev/prod envs

class Config(object):

	# use debug mode?
	DEBUG = True

	# use testing mode?
	TESTING = False

	# database configuration
	REDIS_DB = 0

class Test(Config):
	TESTING = True
	REDIS_DB = 1

class Prod(Config):
	DEBUG = False

class Dev(Config):
	pass