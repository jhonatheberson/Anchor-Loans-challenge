# importing necessary modules
from ma import ma
from marshmallow import fields


class PhotoSchema(ma.Schema):
  """Class responsible for serialization/deserialization the Photo

  Args:
      ma ([marshmallow]): [serialization scheme]
  """  
  likes = fields.Int()
  approved = fields.Int()
  url = fields.Str()
