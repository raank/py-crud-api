import uuid
import datetime

from app.main import db, save, commit, remove
from app.main.model.news import News as Model
from app.main.model.user import User

""" Show all Items """
def all():
    return Model.query.all()

""" Find Items """
def search(string):
    search = "%{}%".format(string)

    return db.session.query(Model, User).filter(News.title.like(search)).filter(News.body.like(search)).filter(User.name.like(search)).all()

""" Store a new Item """
def store(data):
    if data is not None:
        model = Model(
            user_id=data['user_id'],
            title=data['title'],
            body=data['body'],
            created_at=datetime.datetime.utcnow()
        )

        save(model)

        return model, 201
    
    return {
        'status': 'fail',
        'message': 'This is not working'
    }, 400

""" Show a unique Item """
def show(id):
    return Model.query.filter_by(id=id).first()

""" Update a exists Item """
def update(id, data):
    model = show(id)

    if 'title' in data:
        model.title = data['title']

    if 'body' in data:
        model.title = data['title']

    model.updated_at = datetime.datetime.utcnow()

    commit()
    
    return report

""" Remove a Item """
def delete(id):
    model = show(id)

    if model is not None:
        remove(model)
        return True

    return False