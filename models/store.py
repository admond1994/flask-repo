from db import db

# internal workflow (clients don't see this)
class StoreModel(db.Model): # save this object in SQLAlchemy (database)
    __tablename__ = 'stores'

    # define 3 columns to be stored in DB
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # lazy=dynamic --> will only look at the table when JSON method is called (save resource)
    items = db.relationship('ItemModel', lazy='dynamic') # each store has different items 

    def __init__(self, name):
        self.name = name

    def json(self):  # return JSON format (dict) of the model
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        # from the SQLalchemy item mode, query the model based on name and get the first row
        return cls.query.filter_by(name=name).first() # return ItemModel object (or cls)

    def save_to_db(self):
        # session --> collection of objects that we want to write to DB
        db.session.add(self) #   
        db.session.commit()  #

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()