import os
import sys
from flask import Flask
from redis import Redis

#---------------------------------------------
# initialization
# --------------------------------------------

app = Flask(__name__)
app.config.update(
    DEBUG = True,
)

try:
    db = Redis(host='localhost', port=6379, db=1)
except:
    print "Cannot connect to redis server.  Exiting..."
    sys.exit(0)

#---------------------------------------------
# launch
# --------------------------------------------

sys.path.insert(0, '../')

from api import *

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
