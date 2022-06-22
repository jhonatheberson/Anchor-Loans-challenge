from db import db


class User(db.Document):
    name = db.StringField()
    email = db.StringField()
    password = db.StringField()
    level = db.IntField()
    
