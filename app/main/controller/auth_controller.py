from flask import request
from flask_restx import Resource

from app.main.service.auth_helper import Auth
from ..util.dto import AuthDto

api = AuthDto.api
login = AuthDto.login
register = AuthDto.register


@api.route('/login')
class UserLogin(Resource):
    @api.doc('login')
    @api.expect(login, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/register')
class UserRegister(Resource):
    @api.doc('register')
    @api.expect(register, validate=True)
    def post(self):
        post_data = request.json
        return Auth.register_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    @api.doc('logout')
    def post(self):
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)
