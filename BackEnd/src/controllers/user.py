from flask import request, make_response
from flask_restplus import Resource, fields
from werkzeug.security import generate_password_hash
from controllers.session import *

from models.user import User
from schemas.user import UserSchema


from server.instance import server

api = server.api
app = server.app

gallery_ns = server.gallery_ns

user_schemy = UserSchema()
gallery_list_scheme = UserSchema(many=True)

ITEM_NOT_FOUND = 'User not found'

item = gallery_ns.model('User', {
    'name': fields.String(description='Name user'),
    'email': fields.String(description='Loguin user'),
    'password': fields.String(description='Password user'),
    'level': fields.Integer(description='level User')
})


@api.route('/users/')
class ControllerUsers(Resource):
    user = User()
    @token_required
    def get(self, current_user):
        user_data = User.query
        return gallery_list_scheme.dump(user_data), 200


    




@api.route('/user/')
class ControllerUser(Resource):
    @gallery_ns.expect(item)
    @gallery_ns.doc('Create User')
    def post(self, ):

        gallery_json = request.get_json()
        user = User.query.filter(User.email == gallery_json['email']).first()
        
        password_crypt = generate_password_hash(gallery_json['password'])
        if not user:
            User(name=gallery_json['name'], email=gallery_json['email'],
                 password=password_crypt, level=gallery_json['level']).save()

            return make_response('Successfully registered.', 201)
        else:
            return make_response('User already exists. Please Log in.', 202)

    @gallery_ns.expect(item)
    @gallery_ns.doc('Update User')
    @token_required
    def put(self, current_user):
        gallery_json = request.get_json()
        gallery_data = User.query.filter(
            User.email == gallery_json['email']).first()
        
        if gallery_data:
          

          gallery_data.name = gallery_json['name']
          gallery_data.email = gallery_json['email']
          gallery_data.password = generate_password_hash(
              gallery_json['password'])

          gallery_data.save()
          print(gallery_data.name)
          return user_schemy.dump(gallery_data), 200
        else:
          return make_response('User not exists.', 202)

    # @token_required
    def get(self):
        email = request.args.get('email')
        gallery_data = User.query.filter(User.email == email).first(), 200
        if gallery_data:
            return user_schemy.dump(gallery_data[0])
        return {'message': ITEM_NOT_FOUND}, 404

  
    @token_required
    @gallery_ns.doc('Delete User')
    def delete(self, current_user):
        email = request.args.get('email')
        gallery_data = User.query.filter(User.email == email).first()
        if (gallery_data):
            gallery_data.remove()
            return 'deleted user', 204
        return {'message': ITEM_NOT_FOUND}
