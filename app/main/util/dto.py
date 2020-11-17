from flask_restx import Namespace, fields
import os

class UserDto:
    api = Namespace('user', description='Users', base_url=os.getenv('APP_HOST'))
    user = api.model('user', {
        'id': fields.Integer(required=False, description='user id'),
        'public_id': fields.String(description='user Identifier'),
        'email': fields.String(required=True, description='user email address'),
        'name': fields.String(description='user name'),
        'registered_on': fields.String(description='user registration')
    })

class NewsDto:
    api = Namespace('news', description='Reports', base_url=os.getenv('APP_HOST'))
    news = api.model('news', {
        'id': fields.Integer(required=False, description='report id'),
        'user_id': fields.Integer(required=False, description='user id'),
        'title': fields.String(required=True, description='title of report'),
        'body': fields.String(required=True, description='report body'),
        'created_at': fields.String(required=False, description='report created'),
        'updated_at': fields.String(required=False, description='report updated date')
    })

class AuthDto:
    api = Namespace('auth', description='authentication related operations', base_url=os.getenv('APP_HOST'))
    login = api.model('login', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password ')
    })

    register = api.model('register', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
        'name': fields.String(required=True, description='User name')
    })
