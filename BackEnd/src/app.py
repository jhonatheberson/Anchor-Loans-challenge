from flask import jsonify
from marshmallow import ValidationError

from ma import ma
from db import db

# adding controllers
from controllers.user import *
from controllers.session import *

from server.instance import server



if __name__ == '__main__':
  db.init_app(app)
  ma.init_app(app)
  server.run()