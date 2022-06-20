from attr import field
from ma import ma
from marshmallow import fields
from models.gallery import GalleryModel

class GallerySchema(ma.Schema):
  name = fields.Str()
  loguin = fields.Str()
  password = fields.Str()