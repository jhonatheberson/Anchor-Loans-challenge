# importing necessary modules
from flask import request, make_response, redirect, url_for
from flask_restplus import Resource, fields
from controllers.session import token_required, get_token
# importing models
from models.photo import Photo
from models.user import User
# importing schemas
from schemas.photo import PhotoSchema
from schemas.user import UserSchema


# importing class server
from server.instance import server
# starting server modules
api = server.api
app = server.app
# starting server namespace
gallery_ns = server.gallery_ns
# instantiating schemas
photo_schemy = PhotoSchema()
photo_list_scheme = PhotoSchema(many=True)
user_schemy = UserSchema()
# standard messages
ITEM_NOT_FOUND = 'Photo not found'
# template for documentation
Photo = gallery_ns.model('Photo', {
    'url': fields.String(description='url Photo')
})


@api.route('/photos/')
class ControllerPhotos(Resource):
    """class with Photos route methods

    Args:
        Resource ([flask_restplus]): [is an extension for Flask that adds support for quickly building REST APIs.]
    """
    @token_required
    def get(self, current_user):
        """method that lists all photos

        Returns:
            [json]: [returns all photos]
        """
        user_data = Photo.query
        return photo_list_scheme.dump(user_data), 200


@api.route('/photo/')
class ControllerPhoto(Resource):
    """class with Photo route methods

    Args:
        Resource ([flask_restplus]): [is an extension for Flask that adds support for quickly building REST APIs.]
    """
    @gallery_ns.expect(Photo)
    @gallery_ns.doc('Create Photo')
    @token_required
    def post(self, current_user):
        """create the photo

        Returns:
            [json]: [return success or failure message]
        """        
        user = get_token()
        current_user = user_schemy.dump(user)
        user_id = User.query.filter(
            User.email == current_user['email']).first()
        url = request.args.get('url')
        photo = Photo.query.filter(Photo.url == url).first()

        if not photo:
            Photo(approved=0, likes=0,
                  user_id=user_id, url=url).save()

            return make_response('Successfully registered.', 201)
        else:
            return make_response('Photo already exists.', 202)

    @token_required
    @gallery_ns.doc('Delete Photo')
    def delete(self, current_user):
        """delete the photo

        Returns:
            [json]: [return success or failure message]
        """
        url = request.args.get('url')
        photo = Photo.query.filter(
            Photo.url == url).first()
        if (photo):
            photo.remove()
            return 'deleted photo', 204
        return {'message': ITEM_NOT_FOUND}


@api.route('/photo/approve')
class ControllerPhoto(Resource):
    @gallery_ns.expect(Photo)
    @gallery_ns.doc('approve Photo')
    @token_required
    def put(self, current_user):
        """approve the photo

        Returns:
            [json]: [return success or failure message]
        """
        url = request.args.get('url')
        photo = Photo.query.filter(Photo.url == url).first()

        if photo:
            photo.approved = 1
            photo.save()
            return make_response('Approve photo', 200)
        else:
            return make_response('Photo not exists.', 202)


@api.route('/photo/like')
class ControllerPhoto(Resource):
    @gallery_ns.expect(Photo)
    @gallery_ns.doc('Like the Photo')
    @token_required
    def put(self, current_user):
        """liked the photo

        Returns:
            [json]: [return success or failure message]
        """
        url = request.args.get('url')
        photo = Photo.query.filter(Photo.url == url).first()

        if photo:
            photo.likes = photo.likes + 1
            photo.save()
            return make_response('Like the photo', 200)
        else:
            return make_response('Photo not exists.', 202)
