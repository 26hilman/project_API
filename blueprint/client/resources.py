import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from blueprint import db
from flask_jwt_extended import jwt_required

from . import *

bp_client = Blueprint('client', __name__)
api = Api(bp_client)

class ClientResource(Resource):

    def __init__(self):
        pass

    def get(self, id = None):
        if id == None :
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=999)
            args = parser.parse_args()
            
            offset = (args['p'] * args['rp']) - args['rp']

            qry_all = ListClient.query

            list_get_all = []

            for data in qry_all.limit(args['rp']).offset(offset).all() :
                list_get_all.append(marshal(data, ListClient.response_field))
            return list_get_all, 200, {'Content-Type':'application/json'}

        else :
            qry_id = ListClient.query.get(id)
            if qry_id != None :
                return marshal(qry_id, ListClient.response_field), 200, {'Content-Type':'application/json'}
            return {'mode': 'NOT_FOUND'}, 404, {'Content-Type':'application/json'}
    
    # @jwt_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json')
        parser.add_argument('client_secret', location='json')
        parser.add_argument('mode', location='json')
        args = parser.parse_args()

        qry_put = ListClient.query.get(id)
        if qry_put != None :
            qry_put.client_key = args['client_key']
            qry_put.client_secret = args['client_secret']
            qry_put.mode = args['mode']
            db.session.commit()
            return marshal(qry_put, ListClient.response_field), 200, {'Content-Type':'application/json'}
        return {'mode': 'NOT_FOUND'}, 404, {'Content-Type':'application/json'}

    # @jwt_required   
    def delete(self, id):
        qry_delete = ListClient.query.get(id)
        if qry_delete != None :
            db.session.delete(qry_delete)
            db.session.commit()
            return 'Delete Completed', 200, {'Content-Type':'application/json'}
        return {'mode': 'NOT_FOUND'}, 404, {'Content-Type':'application/json'}
    
    # @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json')
        parser.add_argument('client_secret', location='json')
        parser.add_argument('mode', location='json')
        args = parser.parse_args()
        print(args)
        
        list_client = ListClient(None, args['client_key'], args['client_secret'], args['mode'])
        db.session.add(list_client)
        db.session.commit()

        return marshal(list_client, ListClient.response_field), 200, {'Content-Type':'application/json'}
    
api.add_resource(ClientResource, '/client', '/client/<int:id>')