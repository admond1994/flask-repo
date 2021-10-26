import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
# 1st arg (remote env variable), 2nd arg (local env variable)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///data.db') # tell SQLAlchey where to find the DB filem
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # turn off the tracker for SQLalchemy (reduce resources used)
app.secret_key = 'jose'
api = Api(app) # add resource to API (Every resource needs to be a class)

@app.before_first_request  # run the method below before 1st request
def create_tables():
    db.create_all()  # before 1st request is run, create a table

# authenticate user using JWT token
jwt = JWT(app, authenticate, identity) # create an endpoint --> /auth

# create API endpoints by adding resources
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register') # add resource as endpoint


if __name__ == '__main__':
    db.init_app(app)
    # ONLY run the app when it's "__main__" (we explicitly run this file)
    app.run(port=5000, debug=True)