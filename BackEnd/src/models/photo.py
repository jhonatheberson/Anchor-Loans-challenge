# importing necessary modules
from db import db
from models.user import User

class Photo(db.Document):
  """class responsible for manipulating the data in the database in Document Photo

    Args:
        db ([MongoAlchemy]): [bank instance]
  """
  user_id = db.DocumentField(User)
  likes = db.IntField()
  approved = db.IntField()
  url = db.StringField()
