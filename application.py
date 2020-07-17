# -*- coding: utf-8 -*-

from os import getenv
from os.path import dirname, isfile, join


from dotenv import load_dotenv


_ENV_FILE = join(dirname(__file__), '.env')


if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)

from apps import create_app


app = create_app(getenv('FLASK_ENV') or 'default')

if __name__ == '__main__':
    host = 'localhost'
    ip = '0.0.0.0'
    port = app.config['APP_PORT']
    debug = app.config['DEBUG']

    app.run(
        host=host, debug=debug, port=port, use_reloader=debug
    )