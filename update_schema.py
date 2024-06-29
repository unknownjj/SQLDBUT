import sqlite3
import os

# Path to your SQLite database
db_path = os.path.join(os.getcwd(), 'bot_database.db')  # Construct the full path

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add new columns to the tokens table
try:
    cursor.execute("ALTER TABLE tokens ADD COLUMN price FLOAT")
    cursor.execute("ALTER TABLE tokens ADD COLUMN fdv FLOAT")
    cursor.execute("ALTER TABLE tokens ADD COLUMN volume24h FLOAT")
    cursor.execute("ALTER TABLE tokens ADD COLUMN priceChange24h FLOAT")
    print("Columns added successfully.")
except sqlite3.OperationalError as e:
    print(f"An error occurred: {e}")

# Commit the changes and close the connection
conn.commit()
conn.close()