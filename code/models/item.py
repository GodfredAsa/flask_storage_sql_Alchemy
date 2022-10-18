import sqlite3
from constants import DB_PATH


class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            # return {"name": name, "price": row[1]}, 200
            return {"id": row[0], "name": row[1], "price": row[2]}, 200
            # return cls(*row), 200

    def insert_item(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (NULL, ?, ?)"
        cursor.execute(query, (self.name, self.price))
        connection.commit()
        connection.close()

    def update_item(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (self.price, self.name))
        connection.commit()
        connection.close()

