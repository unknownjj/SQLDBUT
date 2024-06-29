import sqlite3
import os

# Path to your SQLite database
db_path = os.path.join(os.getcwd(), 'bot_database.db')  # Construct the full path

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query the table schema
cursor.execute("PRAGMA table_info(tokens)")
columns = cursor.fetchall()

# Print the columns
for column in columns:
    print(column)

# Close the connection
conn.close()