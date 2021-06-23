from ma import ma
from flask_restx import fields

from models.item import ItemModel
from models.store import StoreModel
from api import api


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_only = ('store',)
        dump_only = ('id',)
        load_instance = True
        include_fk = True


itemInputSchema = api.model('ItemModel', {
    'price': fields.Float,
    'store_id': fields.Integer
})
