from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import UserDto
from ..service import user_service as Service

api = UserDto.api
_user = UserDto.user

@api.route('/')
class UserList(Resource):
    @api.doc('index.users')
    @admin_token_required
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        return Service.all()

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('store.users')
    def post(self):
        data = request.json
        return Service.store(data)


@api.route('/<id>')
@api.param('id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @token_required
    @api.marshal_with(_user)
    def get(self, id):
        """get a user given its identifier"""
        user = Service.show(id)
        if not user:
            api.abort(404)
        else:
            return user

    @api.doc('update.users')
    @token_required
    @api.marshal_with(_user)
    def put(self, id):
        """get a user given its identifier"""
        user = Service.show(id)

        if not user:
            api.abort(404)
        else:
            return Service.update(user=user, data=request.json), 200

    @api.doc('delete.users')
    @token_required
    @api.marshal_with(_user)
    def put(self, id):
        """get a user given its identifier"""
        user = Service.show(id)

        if not user:
            api.abort(404)
        else:
            if Service.delete(id):
                response = {
                    'status': 'success',
                    'message': 'Item removed has success'
                }

                return response, 201
            
            return {
                'status': 'fail',
                'message': 'Does nothing possible removing'
            }, 400


