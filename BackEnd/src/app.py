from flask import jsonify
from marshmallow import ValidationError

from ma import ma
from db import db
from controllers.gallery import *

from server.instance import server




# @app.before_first_request
# def create_tables():
#   db.create_all()

# api.route(Gallery, '/gallerys/<int?id>')

if __name__ == '__main__':
  db.init_app(app)
  ma.init_app(app)
  server.run()