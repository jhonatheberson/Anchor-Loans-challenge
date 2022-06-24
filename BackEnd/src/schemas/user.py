from ma import ma
from marshmallow import fields


class UserSchema(ma.Schema):
    name = fields.Str()
    email = fields.Str()
    # password = fields.Str()
    level = fields.Int()
