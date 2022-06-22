from ma import ma
from marshmallow import fields
from schemas.photo import PhotoSchema


class CommentSchema(ma.Schema):
    photo_id = ma.Nested(PhotoSchema)
    commit = fields.Str()
