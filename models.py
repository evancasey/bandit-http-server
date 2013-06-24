import datetime
from bandit import *
from app import db

#---------------------------------------------
# models
# --------------------------------------------



# class User(db.Model, BaseUser):
#     username = CharField()
#     password = CharField()
#     email = CharField()
#     join_date = DateTimeField(default=datetime.datetime.now)
#     active = BooleanField(default=True)
#     admin = BooleanField(default=False)

#     def __unicode__(self):
#         return self.username