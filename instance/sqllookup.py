import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect("C:/Users/mario/AppData\Local/Programs/Python/Flask-API/instance/database.db")

# Create a cursor object
cursor = connection.cursor()

# Query the user_model table structure
cursor.execute("PRAGMA table_info(user_model);")
columns = cursor.fetchall()
print("Columns:", columns)

# Fetch all data from the user_model table
cursor.execute("SELECT * FROM user_model;")
rows = cursor.fetchall()
print("Rows:", rows)

# Close connection
connection.close()
