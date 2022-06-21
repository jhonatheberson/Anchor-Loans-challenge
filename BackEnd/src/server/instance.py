from flask import Flask, Blueprint
from flask_restplus import Api

class Server():
  def __init__(self) -> None:
    pass
    self.app = Flask(__name__)
    self.blueprint = Blueprint('api', __name__, url_prefix='/api')
    self.api = Api(self.blueprint, doc='/doc', title="Friend's gallery")
    self.app.register_blueprint(self.blueprint)
    self.db = None

    try:
      self.app.config['MONGOALCHEMY_DATABASE'] = 'Anchor'
      self.app.config['MONGOALCHEMY_USER'] = 'root'
      self.app.config['MONGOALCHEMY_PASSWORD'] = 'example'
      self.app.config['SECRET_KEY'] = 'your secret key'
    except:
      print("ERROR - Connot connect to db")
    self.gallery_ns = self.gallery_ns()

  def gallery_ns(self,):
    return self.api.namespace(name='Gallery', description='gallery the pictures', path='/')

  def run(self, ):
    self.app.run(
      port=5000,
      debug=True,
      host='0.0.0.0'
    )


server = Server()