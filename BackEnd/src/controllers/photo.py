from flask import request, make_response, redirect, url_for
from flask_restplus import Resource, fields
from controllers.session import token_required, get_token

from models.photo import Photo
from models.user import User
from schemas.photo import PhotoSchema
from schemas.user import UserSchema
from schemas.photoComment import photoCommentSchema


from server.instance import server

api = server.api
app = server.app

gallery_ns = server.gallery_ns

photoComment_schemy = photoCommentSchema()
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

        return photo_list_scheme.dump(user_data), 200
        
@api.route('/photoscommit/')
class ControllerPhotos(Resource):

    @token_required
    def get(self, current_user):
        user_data = Photo.query
        photos = photo_list_scheme.dump(user_data)
        print(photos)
        photoComment_schemy.url = photos[0]['url']
        photoComment_schemy.likes = photos[0]['likes']
        photoComment_schemy.approved = photos[0]['approved']
        request.args = {'url': photos[0]['url']}
        # request.args.insert('url')
        print(request.args)
        url = request.args.get('url')
        print(url)
        responseredirect = redirect('http://localhost:5000/api/comments/')
        print(responseredirect.get_data())
        # print(photoComment_schemy.loads(photoComment_schemy))
        response = photoComment_schemy.dump(photoComment_schemy)
        return response, 200


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
        url = request.args.get('url')
        photo = Photo.query.filter(
            Photo.url == url).first()
        if (photo):
            photo.remove()
            return 'deleted photo', 204
        return {'message': ITEM_NOT_FOUND}


@api.route('/photo/approve')
class ControllerPhoto(Resource):
    @gallery_ns.expect(itemPhoto)
    @gallery_ns.doc('approve Photo')
    @token_required
    def put(self, current_user):
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
    @gallery_ns.expect(itemPhoto)
    @gallery_ns.doc('Like the Photo')
    @token_required
    def put(self, current_user):
        url = request.args.get('url')
        photo = Photo.query.filter(Photo.url ==url).first()

        if photo:
            photo.likes = photo.likes + 1
            photo.save()
            return make_response('Like the photo', 200)
        else:
            return make_response('Photo not exists.', 202)



