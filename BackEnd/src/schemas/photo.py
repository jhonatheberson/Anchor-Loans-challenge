from ma import ma
from marshmallow import fields
from schemas.user import UserSchema


class PhotoSchema(ma.Schema):
    # user_id = ma.Nested(UserSchema)
    likes = fields.Int()
    approved = fields.Int()
    url = fields.Str()
