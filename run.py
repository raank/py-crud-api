from dotenv import load_dotenv
load_dotenv()

import os, unittest, uuid, datetime
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS

from app import blueprint
from app.main import create_app, db, save
from app.main.model import user, blacklist
from app.main.model.user import User

app = create_app(os.getenv('ENVIRONMENT') or 'dev')
CORS(app)
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(port=os.getenv('APP_PORT'), host=os.getenv('APP_HOST'))

@manager.command
def seed():
    items = User.query.all()

    if len(items) == 0 and os.getenv('FLASK_ENV') == 'development':
        user = User(
                public_id=str(uuid.uuid4()),
                name='Admin',
                email='admin@example.com',
                password='12341234',
                admin=True,
                registered_on=datetime.datetime.utcnow()
            )
        save(user)

        print('Admin created!')
        print('email: admin@example.com, password: 12341234')
    else:
        print('No data to seed')

if __name__ == '__main__':
    manager.run()
