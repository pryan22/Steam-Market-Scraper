import sqlite3
import Common as c
from item import item
from driver import Driver

class sql:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.create_table()
        self.collections = Driver.open_json(self)["collections"]

    def create_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            name TEXT,
            skin TEXT,
            price REAL,
            quantity INTEGER,
            wear TEXT,
            is_stattrak BOOLEAN,
            is_Souvenir BOOLEAN
        )
        """
        self.cursor.execute(create_table_sql)

    def add_items(self, items:list[item]):
        for it in items:
            self.add_item(it)

    def add_item(self, item:item):
        insert_sql = """
        INSERT INTO items (name, skin, price, quantity, wear, is_stattrak, is_Souvenir)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        item_data = (
            item._type,
            item.skin,
            item.price,
            item.quan,
            item.wear,
            item.is_stat_track,
            item.is_souvenir
        )
        self.cursor.execute(insert_sql, item_data)

    def stop(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        