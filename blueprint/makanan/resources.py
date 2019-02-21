import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
import json
import requests
import math
from blueprints import db
from blueprints.book import Books
from blueprints.user import Users
from flask_jwt_extended import jwt_required, get_jwt_claims

from . import *

bp_makanan = Blueprint('makanan', __name__)
api = Api(bp_makanan)


class MakananResource(Resource):

    endpointabc = 'https://api.edamam.com'
    app_id = 'b4495ca4'
    app_key = 'f7544995dce9d1614d1e90e9395d29d9'

    
    def post(self):
        if rent_id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('tinggi_badan', type=int, location='args', required=True)
            parser.add_argument('berat_badan', type=int, location='args', required=True)
            parser.add_argument('q', type=int, location='args', default="food")
            args = parser.parse_args()

            overweight = 25
            under_weight = 18

            list_resep = []

            rq = requests.get(self.endpointabc + '/search', params={
                'q': args['q'], 'app_id': self.app_id,'app_key': self.app_key
                })

            for i in range(len(rq.json()['hits'])):
                hasil = dict()
                hasil["label"] = rq.json()["hits"][i]["recipe"]["label"]
                hasil["dietLabels"] = rq.json()["hits"][i]["recipe"]["dietLabels"]
                hasil["healthLabels"] = rq.json()["hits"][i]["recipe"]["healthLabels"]
                hasil["cautions"] = rq.json()["hits"][i]["recipe"]["cautions"]
                hasil["ingredientLines"] = rq.json()["hits"][i]["recipe"]["ingredientLines"]
                hasil["calories"] = rq.json()["hits"][i]["recipe"]["calories"]
                list_resep.append(hasil)

            imt = args['berat_badan'] / (args['tinggi_badan']/100)**2
            kategori_imt = ""
            if imt < under_weight:
                kategori_imt = "under_weight"
            elif imt > overweight :
                kategori_imt = "over_weight"
            else:
                kategori_imt = "normal"


            food = Makanan(None, args['berat_badan'], args['tinggi_badan'], imt, kategori_imt)

            db.session.add(food)
            db.session.commit()

            food = marshal(food, Makanan.response_field)
            food['rekomendasi_makanan'] = list_resep

            return food, 202, { 'Content-Type': 'application/json' }

    
api.add_resource(MakananResource, "", "/<int:rent_id>")

