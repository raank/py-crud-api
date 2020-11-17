import uuid
import datetime

from app.main import db, save, commit
from app.main.model.user import User as Model

""" Show all Items """
def all():
    return Model.query.all()

""" Store a new Item """
def store(data):
    user = Model.query.filter_by(email=data['email']).first()
    if not user:
        model = Model(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            name=data['name'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save(model)
        
        return model, 200

    response_object = {
        'status': 'fail',
        'message': 'User already exists. Please Log in.',
    }
    return response_object, 409


""" Show a unique Item """
def show(id):
    return Model.query.filter_by(id=id).first()

""" Update a exists Item """
def update(id, data):
    model = show(id)

    if 'email' in data and data['email'] != model.email:
        model.email = data['email']

    if 'name' in data and data['name'] != model.name:
        model.name = data['name']

    commit()

    return model

""" Remove a Item """
def delete(id):
    model = show(id)

    if model is not None:
        remove(model)
        return True

    return False

""" Register a new User """
def register(data):
    model = Model(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            name=data['name'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
    
    save(model)

    return generate_token(model)

""" Generate a new Token """
def generate_token(user):
    try:
        # generate the auth token
        auth_token = Model.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401
