# importing necessary modules
from ma import ma
from marshmallow import fields


class photoCommentSchema(ma.Schema):
  """Class responsible for serialization/deserialization the PhotoComment

  Args:
      ma ([marshmallow]): [serialization scheme]
  """  
  likes = fields.Int()
  approved = fields.Int()
  url = fields.Str()
  commits = []
