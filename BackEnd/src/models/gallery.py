from db import db
from server.instance import server



class GalleryModel(db.Document):

  name = db.StringField()
  loguin = db.StringField()
  password = db.StringField()
  # __tablename__ = 'gallery'

  # id = db.Column(db.Integer, primary_key=True)
  # name = db.Column(db.String(80), nullable=False, unique=True)
  # loguin = db.Column(db.String(80), nullable=False, unique=True)
  # password = db.Column(db.String(80), nullable=False)

  # def __init__(self, name, loguin, password) -> None:
  #   super().__init__()
  #   self.name = name
  #   self.loguin = loguin
  #   self.password = password

  # def __repr__(self) -> str:
  #   return f'GalleryModel(name={self.name}, loguin={self.loguin}, password={self.password})'

  # def json(self, ):
  #   return {
  #     'name' : self.name,
  #     'loguin' : self.loguin,
  #     'password' : self.password
  #   }


  # @classmethod
  # def find_by_name(cls, name):
  #   return cls.query.filter_by(name=name).first()

  # @classmethod
  # def find_by_id(cls, id):
  #   return  cls.query.filter_by(id=id).first()

  # @classmethod
  # def find_all(cls, ):
  #   return cls.query.all()

  # def save_to_db(self, ):
  #   db.session.add(self,)
  #   db.session.commit()

  # def delete_from_db(self, ):
  #     db.session.delete(self)
  #     db.session.commit()    
