from flask import request, make_response
from flask_restplus import Resource, fields
from  werkzeug.security import generate_password_hash, check_password_hash
from controllers.session import token_required

from models.user import User
from schemas.user import UserSchema


from server.instance import server

api = server.api
app = server.app

gallery_ns = server.gallery_ns

user_schemy =  UserSchema()
gallery_list_scheme = UserSchema(many=True)

ITEM_NOT_FOUND = 'User not found'

item = gallery_ns.model('User', {
  'name': fields.String(description='Name user'),
  'loguin': fields.String(description='Loguin user'),
  'password': fields.String(description='Password user')
})

@api.route('/user/<string:loguin>')
class Users(Resource):
  
  def get(self, loguin):
    gallery_data = User.query.filter(User.loguin==loguin).first(), 200
    if gallery_data:
      return user_schemy.dump(gallery_data[0])
    return {'message': ITEM_NOT_FOUND}, 404


  @gallery_ns.expect(item)
  @gallery_ns.doc('Update User')
  def put(self, loguin):
    gallery_data =  User.query.filter(User.name == 'jhonat').first()
    gallery_json = request.get_json()

    gallery_data.name = gallery_json['name']
    gallery_data.loguin = gallery_json['loguin']
    gallery_data.password = gallery_json['password']

    gallery_data.save()
    print(gallery_data.name)
    return user_schemy.dump(gallery_data), 200

  @gallery_ns.doc('Delete User')
  def delete(self, loguin):
    gallery_data = User.query.filter(User.loguin == loguin).first()
    if (gallery_data):
      gallery_data.remove()
      return '', 204
    return {'message': ITEM_NOT_FOUND}


@api.route('/user/')
class Users(Resource):
  @gallery_ns.expect(item)
  @gallery_ns.doc('Create User')
  def post(self, ):
    
    gallery_json = request.get_json()
    gallery_data = user_schemy.load(gallery_json)
    user = User.query.filter(User.loguin == gallery_json['loguin']).first() 
    if not user: 
      User(name=gallery_json['name'], loguin=gallery_json['loguin'], password=generate_password_hash(gallery_json['password'])).save()

      return make_response('Successfully registered.'), 201
    else: 
      return make_response('User already exists. Please Log in.', 202)
    
    return user_schemy.dump(gallery_data), 201
  
  @token_required
  def get(self, ):
    user_data = User.query
    print(user_data[0])
    return gallery_list_scheme.dump(user_data), 200