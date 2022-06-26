# importing necessary modules
from db import db
from models.photo import Photo


class Comment(db.Document):
  """class responsible for manipulating the data in the database in Document Comment

  Args:
      db ([MongoAlchemy]): [bank instance]
  """
  photo_id = db.DocumentField(Photo)
  commit = db.StringField()
