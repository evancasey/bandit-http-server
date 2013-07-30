import sys
import os
from optparse import OptionParser
from api import *
import pdb

#---------------------------------------------
# launch
# --------------------------------------------

if __name__ == "__main__":
	from app import start_app
	import config

	# decide which environment to set up
	parser = OptionParser()
	parser.add_option("--test", action="store_true", dest="test_mode") 
	parser.add_option("--prod", action="store_true", dest="prod_mode") 
	# ... add other options here

	(options,args) = parser.parse_args()

	app = None
	if options.test_mode:
		app = start_app(config.Test)
	elif options.prod_mode:
		app = start_app(config.Prod)
	else:
		app = start_app(config.Dev) # default is Dev env

	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
