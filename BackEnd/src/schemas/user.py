# importing necessary modules
from ma import ma
from marshmallow import fields


class UserSchema(ma.Schema):
  """Class responsible for serialization/deserialization the User

  Args:
      ma ([marshmallow]): [serialization scheme]
  """  
  name = fields.Str()
  email = fields.Str()
  level = fields.Int()
