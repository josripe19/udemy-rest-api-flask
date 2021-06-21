from typing import List

from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), unique=True, nullable=False)
    items = db.relationship('ItemModel', lazy='dynamic')

    @classmethod
    def find_item(cls, name: str) -> 'StoreModel':
        return cls.query.filter_by(name=name).first()

    def upsert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls) -> List['StoreModel']:
        return cls.query.all()
