from werkzeug.security import safe_str_cmp
from models.user import UserModel


# authenticate user (after /auth endpoint is hit)
def authenticate(username, password):
    user = UserModel.find_by_username(username) # get user details, else return None
    if user and safe_str_cmp(user.password, password): # safer way of comparing strings
        return user  # this is used to generate JWT token and sent to the user

# when user requests an endpoint that needs authentication (JWT token)
# "identity" function will not be called unless we decorate our endpoints with the 
# @jwt_required() decorator before our HTTP methods
def identity(payload): # payload --> content of JTW token
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
