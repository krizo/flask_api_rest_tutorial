import sqlite3
from section6.db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name, self.price = name, price


    def json(self):
        return {
            "name": self.name,
            "price": self.price
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # select * from items where name=name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self, 201

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()