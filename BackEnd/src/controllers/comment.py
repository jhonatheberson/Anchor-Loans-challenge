from flask import request, make_response
from flask_restplus import Resource, fields
from werkzeug.security import generate_password_hash
from controllers.session import token_required, get_token

from models.comment import Comment
from models.photo import Photo
from models.user import User
from schemas.comment import CommentSchema
from schemas.photo import PhotoSchema


from server.instance import server

api = server.api
app = server.app

gallery_ns = server.gallery_ns

photo_schemy = CommentSchema()
comment_list_scheme = CommentSchema(many=True)
photo_schemy = PhotoSchema()

ITEM_NOT_FOUND = 'Comment not found'

item = gallery_ns.model('Comment', {
    'photo_id': fields.String(description='photo who registered the Comment'),
    'commit': fields.String(description='url Comment')
})

itemCommit = gallery_ns.model('itemCommit', {
    'commit': fields.String(description='Comment'),
    'url': fields.String(description='url Comment')
})


@api.route('/comments/')
class ControllerComments(Resource):

    @token_required
    def get(self, current_user):
        url = request.args.get('url')
        user_data = Comment.query.filter(Comment.photo_id.url == url)
        return comment_list_scheme.dump(user_data), 200


@api.route('/comment/')
class ControllerComment(Resource):
    @gallery_ns.expect(itemCommit)
    @gallery_ns.doc('Create Comment')
    @token_required
    def post(self, current_user):
        body = request.get_json()
        print(body)
        photo = Photo.query.filter(
            Photo.url == body['url']).first()
        print(photo)
        if photo:
            Comment(photo_id=photo, commit=body['commit']).save()
            return make_response('Successfully registered.', 201)
        else:
            return make_response('Photo does not exist to be commented.', 202)

    @token_required
    @gallery_ns.doc('Delete Comment')
    def delete(self, current_user):
        commit = request.args.get('commit')
        objCommit = Comment.query.filter(
            Comment.commit == commit).first()
        if (objCommit):
            objCommit.remove()
            return 'deleted Comment', 204
        return {'message': ITEM_NOT_FOUND}






