# importing necessary modules
from ma import ma
from db import db

# adding controllers
from controllers.user import *
from controllers.session import *
from controllers.photo import *
from controllers.comment import *


#importing server instance
from server.instance import server


if __name__ == '__main__':
    # starting bank connection
    db.init_app(app)
    # starting library Marshmallow settings
    ma.init_app(app)
    # starting server instance
    server.run()
