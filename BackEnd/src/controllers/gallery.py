from flask import request
from flask_restplus import Resource, fields

from models.gallery import GalleryModel
from schemas.gallery import GallerySchema


from server.instance import server

api = server.api
app = server.app

gallery_ns = server.gallery_ns

gallery_schemy =  GallerySchema()
gallery_list_scheme = GallerySchema(many=True)

ITEM_NOT_FOUND = 'Gallery not found'

item = gallery_ns.model('Gallery', {
  'name': fields.String(description='Name user'),
  'loguin': fields.String(description='Loguin user'),
  'paswword': fields.String(description='Password user')
})

@api.route('/gallerys/<int:id>')
class Gallery(Resource):
  
  def get(self, id):
    gallery_data = GalleryModel.find_by_id(id), 200
    if gallery_data:
      return gallery_schemy.dump(gallery_data)
    return {'message': ITEM_NOT_FOUND}, 404

  @gallery_ns.expect(item)
  @gallery_ns.doc('Update User')
  def put(self, id):
    gallery_data =  GalleryModel.find_by_id(id)
    gallery_json = request.get_json()

    gallery_data.name = gallery_json['name']
    gallery_data.loguin = gallery_json['loguin']
    gallery_data.password = gallery_json['password']

    gallery_data.save_to_db()
    return gallery_schemy.dump(gallery_data), 200

  @gallery_ns.doc('Delete User')
  def delete(self, id):
    gallery_data = GalleryModel.find_by_id(id)
    if (gallery_data):
      gallery_data.delete_from_db()
      return '', 204
    return {'message': ITEM_NOT_FOUND}


@api.route('/gallerys/')
class Gallery(Resource):
  @gallery_ns.expect(item)
  @gallery_ns.doc('Create User')
  def post(self, ):
    gallery_json = request.get_json()
    gallery_data = gallery_schemy.load(gallery_json)

    gallere_data = gallery_data.save_to_db()
    return gallery_schemy.dump(gallery_data), 201

  def get(self, ):
    return gallery_schemy.dump(GalleryModel.find_all()), 200