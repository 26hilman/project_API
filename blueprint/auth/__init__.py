import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprint.client import *

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class CreateTokenResources(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='args', required=True)
        parser.add_argument('client_secret', location='args', required=True)
        args = parser.parse_args()
        
        qry = ListClient.query.filter_by(client_key=args['client_key']).filter_by(client_secret=args['client_secret']).first()
        if qry != None :
            token = create_access_token(marshal(qry, ListClient.response_field))
        else : 
            return {'status':'UNAUTHORIZED', 'message':'invalid key or secret'}, 401
        return {'token': token}, 200

api.add_resource(CreateTokenResources, '/token')
        