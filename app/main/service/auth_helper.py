from app.main.model.user import User
from ..service.blacklist_service import save_token
from ..service.user_service import register

class Auth:

    def register_user(data):
        try:
            user = User.query.filter_by(email=data.get('email')).first()

            if user is None:
                return register(data)

            return {
                'status': 'fail',
                'message': 'User already exists'
            }, 400
    
        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
                'ss': str(e)
            }
            return response_object, 500

    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = User.encode_auth_token(user.id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode()
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):
        if " " in data:
            auth_token = data.split(' ')[1]
        elif data is not None:
            auth_token = data
        else:
            auth_token = ''

        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_user(request):
        token = request.headers.get('Authorization')

        if token is None: return None

        resp = User.decode_auth_token(token)

        if not isinstance(resp, str) and resp is not None:
            user = User.query.filter_by(id=resp).first()
            
            return user

        return None

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)

            if not isinstance(resp, str) and resp is not None:
                user = User.query.filter_by(id=resp).first()
                if user is None:
                    response_object = {
                        'status': 'fail',
                        'message': 'Provide a valid auth token.'
                    }
                    return response_object, 401

                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': str(user.registered_on)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
