import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from constants import DB_PATH
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item
        return {"message": "{} not found".format(name)}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'item': "An item with name '{}' already exists. ".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"])

        try:
            item.insert_item()
        except:
            return {"message": "an error occurred inserting item"}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if not item:
            return {'message': "Item not found"}
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {"message": "item successfully deleted"}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        new_item = ItemModel(name, data["price"])
        if item is None:
            try:
                new_item.insert_item()
            except:
                return {"message": "an error occurred inserting item"}, 500
        else:
            try:
                # needs to be improved
                new_item.update_item()
            except:
                return {"message": "an error occurred updating item"}, 500
        return new_item.json(), 200


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = [{"id": item[0], "name": item[1], "price": item[2]} for item in result]
        connection.close()

        return items, 200
