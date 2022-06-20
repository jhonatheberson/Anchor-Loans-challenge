from db import db

class User(db.Document):
    name = db.StringField()
    loguin = db.StringField()
    password = db.StringField()