from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.items import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                help='Field cant be empty')

    parser.add_argument('store_id', type=int, required=True,
                        help='Every item needs a store id')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'item does not exist'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message':f'An item with name{name} already exists'}, 400

        data = Item.parser.parse_args()
        new_item = ItemModel(name, data['price'], data['store_id'])

        try:
            new_item.save_to_db()
        except:
            return {'message':'An error occured inserting the item'}, 500

        return new_item.json(), 201
        
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message':'Item has been delted'}
        
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if not item:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
