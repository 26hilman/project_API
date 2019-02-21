from blueprint import db
from flask_restful import fields

class ListClient(db.Model):

    __tablename__ = "ListClient"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    client_key = db.Column(db.String(255))
    client_secret = db.Column(db.String(255))
    mode = db.Column(db.String(10))

    response_field = {
        'id' : fields.Integer,
        'client_key' : fields.String,
        'client_secret' : fields.String,
        'mode' : fields.String
    }
    def __init__(self, id, client_key, client_secret, mode):
        print(client_key)
        self.id = id
        self.client_key = client_key
        self.client_secret = client_secret
        self.mode = mode

    def __repr__(self):
        return '<Client %r>' % self.id