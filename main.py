from app import app, db, os
# from api import api
# from models import *
from views import *
from api import *

# api.setup()

#---------------------------------------------
# launch
# --------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)