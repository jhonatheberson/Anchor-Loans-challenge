# importing necessary modules
from ma import ma
from marshmallow import fields
from schemas.photo import PhotoSchema


class CommentSchema(ma.Schema):
  """Class responsible for serialization/deserialization the Comment

  Args:
      ma ([marshmallow]): [serialization scheme]
  """
  commit = fields.Str()
