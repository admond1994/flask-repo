import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

# let new user sign up
class UserRegister(Resource):
    parser = reqparse.RequestParser() # init object to parse our request
    
    parser.add_argument('username',      # make sure "username" arg is there
                        type=str,  
                        required=True, # ensure every request has "username"
                        help="This field cannot be blank!")  # error message (when wrong arg is input)

    parser.add_argument('password',      # make sure "password" arg is there
                        type=str,  
                        required=True, # ensure every request has "password"
                        help="This field cannot be blank!")  # error message (when wrong arg is input)

    def post(self):
        data = UserRegister.parser.parse_args() # parse the arg that comes through JSON payload

        # check if there is a duplicated username before creating a new user in the DB
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400 

        user = UserModel(**data)  # data['username'], data['password']
        user.save_to_db()

        return {"message": "User created successfully."}, 201  # 201 means successfully created
