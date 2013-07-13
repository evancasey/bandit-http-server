import sys
import os
from optparse import OptionParser
from app import app, init_db
from api import *

#---------------------------------------------
# launch
# --------------------------------------------

if __name__ == "__main__":

	# decide if test or development db

	parser = OptionParser()
	parser.add_option("--test", action="store_true", dest="test_mode")
	(options,args) = parser.parse_args()

	if options.test_mode:
		app.config.update(TESTING = True)

	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)