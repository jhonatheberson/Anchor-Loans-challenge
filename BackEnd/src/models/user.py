# importing necessary modules
from db import db


class User(db.Document):
  """class responsible for manipulating the data in the database in Document User

    Args:
        db ([MongoAlchemy]): [bank instance]
  """
  name = db.StringField()
  email = db.StringField()
  password = db.StringField()
  level = db.IntField()
    
