from flask import request, make_response
from flask_restplus import Resource, fields
from werkzeug.security import generate_password_hash
from controllers.session import token_required, get_token

from models.photo import Photo
from models.user import User
from schemas.photo import PhotoSchema
from schemas.user import UserSchema


from server.instance import server

api = server.api
app = server.app

gallery_ns = server.gallery_ns

photo_schemy = PhotoSchema()
photo_list_scheme = PhotoSchema(many=True)
user_schemy = UserSchema()

ITEM_NOT_FOUND = 'Photo not found'

item = gallery_ns.model('Photo', {
    'user_id': fields.String(description='user who registered the photo'),
    'likes': fields.Integer(description='number likes photo'),
    'approved': fields.Integer(description='status photo'),
    'url': fields.String(description='url Photo')
})

itemPhoto = gallery_ns.model('itemPhoto', {
    'url': fields.String(description='url Photo')
})


@api.route('/photos/')
class ControllerPhotos(Resource):

    @token_required
    def get(self, current_user):
        user_data = Photo.query
        # print(user_data[0])
        return gallery_list_scheme.dump(user_data), 200


@api.route('/photo/')
class ControllerPhoto(Resource):
    @gallery_ns.expect(itemPhoto)
    @gallery_ns.doc('Create Photo')
    @token_required
    def post(self, current_user):
        user = get_token()
        current_user = user_schemy.dump(user)
        user_id = User.query.filter(
            User.email == current_user['email']).first()
        gallery_json = request.get_json()
        photo = Photo.query.filter(Photo.url == gallery_json['url']).first()

        if not photo:
            Photo(approved=0, likes=0,
                  user_id=user_id, url=gallery_json['url']).save()

            return make_response('Successfully registered.', 201)
        else:
            return make_response('Photo already exists.', 202)


@api.route('/photo/approve')
class ControllerPhoto(Resource):
    @gallery_ns.expect(itemPhoto)
    @gallery_ns.doc('approve Photo')
    @token_required
    def put(self, current_user):
        user = get_token()
        current_user = user_schemy.dump(user)
        user_id = User.query.filter(
            User.email == current_user['email']).first()
        gallery_json = request.get_json()
        photo = Photo.query.filter(Photo.url == gallery_json['url']).first()

        if photo:
            photo.approved = 1
            photo.save()
            return make_response('Approve photo', 200)
        else:
            return make_response('Photo not exists.', 202)


@api.route('/photo/like')
class ControllerPhoto(Resource):
    @gallery_ns.expect(itemPhoto)
    @gallery_ns.doc('approve Photo')
    @token_required
    def put(self, current_user):
        user = get_token()
        current_user = user_schemy.dump(user)
        user_id = User.query.filter(
            User.email == current_user['email']).first()
        gallery_json = request.get_json()
        photo = Photo.query.filter(Photo.url == gallery_json['url']).first()

        if photo:
            photo.likes = photo.likes+ 1
            photo.save()
            return make_response('Approve photo', 200)
        else:
            return make_response('Photo not exists.', 202)

    # @token_required
    def get(self):
        email = request.args.get('email')
        gallery_data = Photo.query.filter(Photo.email == email).first(), 200
        if gallery_data:
            return user_schemy.dump(gallery_data[0])
        return {'message': ITEM_NOT_FOUND}, 404

    @token_required
    @gallery_ns.doc('Delete Photo')
    def delete(self, current_user):
        email = request.args.get('email')
        gallery_data = Photo.query.filter(Photo.email == email).first()
        if (gallery_data):
            gallery_data.remove()
            return 'deleted photo', 204
        return {'message': ITEM_NOT_FOUND}
