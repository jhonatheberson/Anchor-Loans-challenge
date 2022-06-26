# importing necessary modules
from flask import request, make_response
from flask_restplus import Resource, fields
from controllers.session import token_required
# importing models
from models.comment import Comment
from models.photo import Photo
# importing models
from schemas.comment import CommentSchema
from schemas.photo import PhotoSchema

# importing class server
from server.instance import server
# starting server modules
api = server.api
app = server.app
# starting server namespace
gallery_ns = server.gallery_ns
# instantiating schemas
photo_schemy = CommentSchema()
comment_list_scheme = CommentSchema(many=True)
photo_schemy = PhotoSchema()
# standard messages
ITEM_NOT_FOUND = 'Comment not found'
# template for documentation
Commit = gallery_ns.model('Commit', {
    'commit': fields.String(description='Comment'),
    'url': fields.String(description='url Comment')
})


@api.route('/comments/')
class ControllerComments(Resource):

    @token_required
    def get(self, current_user):
        """method that lists all commits


        Returns:
            [json]: [returns all commits]
        """
        url = request.args.get('url')
        user_data = Comment.query.filter(Comment.photo_id.url == url)
        return comment_list_scheme.dump(user_data), 200


@api.route('/comment/')
class ControllerComment(Resource):
    @gallery_ns.expect(Commit)
    @gallery_ns.doc('Create Comment')
    @token_required
    def post(self, current_user):
        """method create the commit


        Returns:
            [json]: [return success or failure message]
        """
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
        """method delete the commit


        Returns:
            [json]: [return success or failure message]
        """
        commit = request.args.get('commit')
        objCommit = Comment.query.filter(
            Comment.commit == commit).first()
        if (objCommit):
            objCommit.remove()
            return 'deleted Comment', 204
        return {'message': ITEM_NOT_FOUND}
