from db import db

# internal workflow (clients don't see this)
class ItemModel(db.Model): # save this object in SQLAlchemy (database)
    __tablename__ = 'items'

    # define 3 columns to be stored in DB
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) # each item belongs to what store
    store = db.relationship('StoreModel') # every item has a store that matches with the "store.id" in Store table 

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):  # return JSON format (dict) of the model
        return {'name': self.name, 'price': self.price}

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