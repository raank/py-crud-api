from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.news_controller import api as news_ns

import os

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title=os.getenv('APP_NAME'),
          version=os.getenv('APP_VERSION')
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(news_ns, path='/news')