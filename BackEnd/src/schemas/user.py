from attr import field
from ma import ma
from marshmallow import fields

class UserSchema(ma.Schema):
  name = fields.Str()
  loguin = fields.Str()
  password = fields.Str()