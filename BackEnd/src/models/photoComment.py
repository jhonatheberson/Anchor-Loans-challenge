from db import db
from models.comment import Comment


class photoComment(db.Document):
    likes = db.IntField()
    approved = db.IntField()
    url = db.StringField()
    user_id = db.DocumentField(Comment)
