# importing necessary modules
from flask import request, make_response, jsonify
from jwt.exceptions import ExpiredSignatureError
from flask_restplus import Resource, fields
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
# importing models
from models.user import User
# importing schemas
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
itemSession = gallery_ns.model('Session', {
    'email': fields.String(description='Loguin user'),
    'password': fields.String(description='Password user')
})


def get_token():
    """function that returns the token

    Returns:
        [model]: [returns user information]
    """
    token = None
    token = request.headers['Authorization'].split(" ")[1]

    try:
        data = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256', ],)
    except ExpiredSignatureError as error:
        return make_response('expired token', 401)
    current_user = User.query.filter(
        User.email == data['public_id']).first()
    return current_user


def token_required(f):
    """Middleware to verify authentication

    Args:
        f ([decorated]): [description]

    Returns:
        [decorated]: [returns user information]
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        try:
            token = request.headers['Authorization'].split(" ")[1]
        except:
            return make_response('Token is missing', 401)

        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=['HS256', ],)
        except ExpiredSignatureError as error:
            return make_response('expired token', 401)
        current_user = User.query.filter(
            User.email == data['public_id']).first()
        return f(user_schemy.dump(current_user), *args, **kwargs)

    return decorated


@api.route('/session/')
class Sessions(Resource):
    """that authentication class

    Args:
        Resource ([flask_restplus]): [is an extension for Flask that adds support for quickly building REST APIs.]
    """
    @gallery_ns.doc('user authentication')
    @gallery_ns.expect(itemSession)
    def post(self, ):
        """create the session and return jwt token

        Returns:
            [json]: [return jwt token]
        """
        auth = request.get_json()

        if not auth or not auth['email'] or not auth['password']:
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
            )

        user = User.query.filter(User.email == auth['email']).first()

        if not user:
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
            )

        if check_password_hash(user.password, auth['password']):
            token = jwt.encode({
                'public_id': user.email,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            return make_response(jsonify({'token': token}), 201)

        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
        )
