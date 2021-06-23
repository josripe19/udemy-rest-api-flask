from ma import ma
from flask_restx import fields

from models.user import UserModel
from api import api


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ('password',)
        dump_only = ('id',)
        load_instance = True


userAuthSchema = api.model('UserModel', {
    'username': fields.String,
    'password': fields.String
})
