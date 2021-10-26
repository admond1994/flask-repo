from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource): # create a resource (Student)
    # check to make sure the right arg is passed as JSON payload to the endpoint
    parser = reqparse.RequestParser() # init object to parse our request
    parser.add_argument('price',      # make sure "price" arg is there
                        type=float,  
                        required=True, # ensure every request has price
                        help="This field cannot be left blank!")  # error message (when wrong arg is input)
    
    parser.add_argument('store_id',      # make sure "price" arg is there
                        type=int,  
                        required=True, # ensure every request has price
                        help="Every item needs a store ID")

    @jwt_required()  # need to authenticate before we call GET method
    def get(self, name):
        item = ItemModel.find_by_name(name) # return an object
        if item:
            return item.json()  # return a dict
        return {'message': 'Item not found'}

    def post(self, name):        
        if ItemModel.find_by_name(name):
            # if matched item is found, then return this message
            return {'message': 'An item with name {} already exists'.format(name)}, 400 # bad request

        data = Item.parser.parse_args() # parse the arg that comes through JSON payload

        item = ItemModel(name, **data)  # data['price'], data['store_id']
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500 # internal server error
        
        return item.json(), 201  # tell client that a new resource is created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args() # parse the arg that comes through JSON payload

        # check if item already exists in DB
        item = ItemModel.find_by_name(name)

        if item is None: # if no item yet, then insert it in DB
            item = ItemModel(name, **data) # data['price'], data['store_id']

        else: # if item already exists, then update the item
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        # for each object, convert to JSON
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        # OR --> return {'items': [item.json() for item in ItemModel.query.all()]}