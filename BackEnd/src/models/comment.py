from db import db
from models.photo import Photo


class Comment(db.Document):
    photo_id = db.DocumentField(Photo)
    commit = db.StringField()
