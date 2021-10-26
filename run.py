from app import app
from db import db

db.init_app(app)

@app.before_first_request  # run the method below before 1st request
def create_tables():
    db.create_all()  # before 1st request is run, create a table