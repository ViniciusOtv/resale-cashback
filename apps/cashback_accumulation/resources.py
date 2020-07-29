import requests
from flask import request
import json

from os import getenv
from os.path import dirname, isfile, join

from flask_restful import Resource


from apps.responses import (
    resp_already_exists,
    resp_exception,
    resp_data_invalid,
    resp_ok
)


class Accumulation(Resource):

    def get(self, document):
        _ENV_FILE = join(dirname(__file__), '.env')

        if isfile(_ENV_FILE):
            load_dotenv(dotenv_path=_ENV_FILE)

        uri = getenv('URI_CASHBACK')

        token = getenv('API_TOKEN')

        headers = {'Content-Type': 'application/json',
                   'Authorization': '{0}'.format(token)
                   }

        response = requests.get(uri + document)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return response.status_code
