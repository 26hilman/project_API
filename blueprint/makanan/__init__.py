from blueprint import db
from flask_restful import fields

class Makanan(db.Model):

    __tablename__ = "ListMakanan"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    berat_badan = db.Column(db.Integer)
    tinggi_badan = db.Column(db.Integer)
    angka_imt = db.Column(db.Integer)
    kategori_imt = db.Column(db.String(255))

    response_field = {
        'id' = fields.Integer,
        'berat_badan' = fields.Integer,
        'tinggi_badan' = fields.Integer,
        'angka_imt' = fields.Integer,
        'kategori_imt' = fields.String
    }

    def __init__(self, id, berat_badan, tinggi_badan, angka_imt, kategori_imt):
        self.id = id
        self.berat_badan = berat_badan
        self.tinggi_badan = tinggi_badan
        self.angka_imt = angka_imt
        self.kategori_imt = kategori_imt
    
    def __repr__(self):
        return '<Makanan %r>' % self.id
