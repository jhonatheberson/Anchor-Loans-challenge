from ma import ma
from marshmallow import fields
from schemas.comment import CommentSchema


class photoCommentSchema(ma.Schema):
        # fields = ('likes', 'approved', 'url', 'commits')
    likes = fields.Int()
    approved = fields.Int()
    url = fields.Str()
    commits = []