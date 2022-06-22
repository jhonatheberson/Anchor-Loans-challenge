from db import db
from models.user import User

class Photo(db.Document):
    user_id = db.DocumentField(User)
    likes = db.IntField()
    approved = db.IntField()
    url = db.StringField()
