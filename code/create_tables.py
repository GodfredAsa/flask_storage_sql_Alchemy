import sqlite3

connection = sqlite3.connect("./code/data.db")
cursor = connection.cursor()
create_table = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)
connection.commit()
connection.close()

# when creating a user no need to specify the id as we are using auto increment
# real is a decimal number in sql3lite example 10.99
