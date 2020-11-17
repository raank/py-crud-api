from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import NewsDto
from ..service import news_service as Service
from ..service.auth_helper import Auth

api = NewsDto.api
_news = NewsDto.news

@api.route('/')
class NewsList(Resource):

    @api.doc('index.report')
    @api.marshal_list_with(_news, envelope='data')
    def get(self):
        """List all registered Reports"""
        return Service.all()

    @api.expect(_news, validate=True)
    @api.response(201, 'Report successfully created.')
    @token_required
    @api.doc('store.report')
    @api.marshal_with(_news)
    def post(self):
        user = Auth.get_user(request)

        if user is None:
            response_object = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return response_object, 409

        body = request.json
        data = {
            'user_id': user.id,
            'title': body.get('title'),
            'body': body.get('body')
        }

        return Service.store(data)

@api.route('/<id>')
@api.param('id', 'The report identifier')
@api.response(404, 'Report not found.')
class NewsItem(Resource):
    @api.doc('show.report')
    @api.marshal_with(_news, envelope='data')
    def get(self, id):
        report = Service.show(id)

        if not report:
            api.abort(404)
        else:
            return report


    @api.doc('update.report')
    @api.marshal_with(_news, envelope='data')
    def put(self, id):
        report = Service.show(id)

        if not report:
            api.abort(404)
        else:
            return Service.update(id, request.json)

    @api.doc('delete.report')
    @admin_token_required
    def delete(self, id):
        report = Service.show(id)

        if not report:
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