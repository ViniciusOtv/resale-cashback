# -*- coding: utf-8 -*-

from flask import Flask
from config import config

from .api import configure_api
from .db import db
from .jwt import configure_jwt

def create_app(config_name):
    app = Flask('api-users')

    app.config.from_object(config[config_name])

    # Configurando MongoEngine
    db.init_app(app)

    # Configurando JWT
    configure_jwt(app)

    configure_api(app)

    return app