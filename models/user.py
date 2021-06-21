from typing import List, Dict, Union
from werkzeug.security import generate_password_hash, check_password_hash

from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    def __str__(self):
        return f"<User id: {self.id}, username: {self.username}>"

    def encrypt_password(self):
        self.password = generate_password_hash(self.password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls) -> List['UserModel']:
        return cls.query.all()

    @classmethod
    def find_by_username(cls, username: str) -> 'UserModel':
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> 'UserModel':
        return cls.query.filter_by(id=_id).first()
