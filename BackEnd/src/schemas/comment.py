from ma import ma
from marshmallow import fields
from schemas.photo import PhotoSchema


class CommentSchema(ma.Schema):
    commit = fields.Str()
