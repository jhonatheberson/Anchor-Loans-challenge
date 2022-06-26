# importing necessary modules
from flask import request, make_response
from flask_restplus import Resource, fields
from werkzeug.security import generate_password_hash
# importing controllers
from controllers.session import *
# importing models
from models.user import User
# importing models
from schemas.user import UserSchema

# importing class server
from server.instance import server

# starting server modules
api = server.api
app = server.app
# starting server namespace
gallery_ns = server.gallery_ns
# instantiating schemas
user_schemy = UserSchema()
gallery_list_scheme = UserSchema(many=True)
# standard messages
ITEM_NOT_FOUND = 'User not found'
# template for documentation
item = gallery_ns.model('User', {
    'name': fields.String(description='Name user'),
    'email': fields.String(description='Loguin user'),
    'password': fields.String(description='Password user'),
    'level': fields.Integer(description='level User')
})


@api.route('/users/')
class ControllerUsers(Resource):
    """class with users route methods

    Args:
        Resource ([flask_restplus]): [is an extension for Flask that adds support for quickly building REST APIs.]
    """

    @token_required
    @gallery_ns.doc('Delete Users')
    def get(self, current_user):
        """method that lists all users


        Returns:
            [json]: [returns the deserialized object users]
        """
        user_data = User.query
        return gallery_list_scheme.dump(user_data), 200


@api.route('/user/')
class ControllerUser(Resource):
    """class with user route methods

    Args:
        Resource ([flask_restplus]): [is an extension for Flask that adds support for quickly building REST APIs.]
    """
    @gallery_ns.expect(item)
    @gallery_ns.doc('Create User')
    def post(self, ):
        """method that create user

        Returns:
            [json]: [returns the deserialized object user]
        """
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
        """method that update user

        Returns:
            [json]: [returns the deserialized object user]
        """
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

    @token_required
    @gallery_ns.doc('Get User')
    def get(self):
        """method that get user

        Returns:
            [json]: [returns the deserialized object user]
        """
        email = request.args.get('email')
        gallery_data = User.query.filter(User.email == email).first(), 200
        if gallery_data:
            return user_schemy.dump(gallery_data[0])
        return {'message': ITEM_NOT_FOUND}, 404

    @token_required
    @gallery_ns.doc('Delete User')
    def delete(self, current_user):
        """method that delete user

        Returns:
            [json]: [returns the deserialized object user]
        """
        email = request.args.get('email')
        gallery_data = User.query.filter(User.email == email).first()
        if (gallery_data):
            gallery_data.remove()
            return 'deleted user', 204
        return {'message': ITEM_NOT_FOUND}
