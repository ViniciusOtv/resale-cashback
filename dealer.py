from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine('sqlite:///teste-boticario.db')
app = Flask(__name__)
api = Api(app)

class Dealer(Resource): 
    def post(self):
            conn = db_connect.connect()
            name = request.json["name"]
            document = request.json["document"]
            email = request.json["email"]
            password = request.json["password"]
            confirm_password = request.json["confirm_password"]

            conn.execute(
                "insert into dealer values(null, '{0}', '{1}', '{3}', '{4}'".format()
            )