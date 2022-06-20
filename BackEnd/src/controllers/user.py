from flask import request
from flask_restplus import Resource, fields

from models.user import User
from schemas.user import UserSchema


from server.instance import server

api = server.api
app = server.app

gallery_ns = server.gallery_ns

gallery_schemy =  UserSchema()
gallery_list_scheme = UserSchema(many=True)

ITEM_NOT_FOUND = 'User not found'

item = gallery_ns.model('User', {
  'name': fields.String(description='Name user'),
  'loguin': fields.String(description='Loguin user'),
  'password': fields.String(description='Password user')
})

@api.route('/user/<int:id>')
class Users(Resource):
  
  def get(self, id):
    gallery_data = User.find_by_id(id), 200
    if gallery_data:
      return gallery_schemy.dump(gallery_data)
    return {'message': ITEM_NOT_FOUND}, 404


  @gallery_ns.expect(item)
  @gallery_ns.doc('Update User')
  def put(self, id):
    # gallery_data =  User.find_by_id(id)
    # gallery_json = request.get_json()

    # gallery_data.name = gallery_json['name']
    # gallery_data.loguin = gallery_json['loguin']
    # gallery_data.password = gallery_json['password']

    # gallery_data.save_to_db()
    mark = User(name='jhonat', loguin='jhonat@gmail.com', password='1234')
    mark.save()
    return gallery_schemy.dump(mark), 200

  @gallery_ns.doc('Delete User')
  def delete(self, id):
    gallery_data = User.find_by_id(id)
    if (gallery_data):
      gallery_data.delete_from_db()
      return '', 204
    return {'message': ITEM_NOT_FOUND}


@api.route('/user/')
class Users(Resource):
  @gallery_ns.expect(item)
  @gallery_ns.doc('Create User')
  def post(self, ):
    gallery_json = request.get_json()
    gallery_data = gallery_schemy.load(gallery_json)

    gallere_data = gallery_data.save_to_db()
    return gallery_schemy.dump(gallery_data), 201

  def get(self, ):
    return gallery_schemy.dump(User.query), 200