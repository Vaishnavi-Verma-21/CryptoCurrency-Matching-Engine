import sqlite3

# Connect to the database (will create it if it doesn't exist)
conn = sqlite3.connect("trades.db")

# Read SQL schema from file
with open("schema.sql", "r") as f:
    schema = f.read()

# Execute the schema
conn.executescript(schema)
conn.commit()
conn.close()

print("✅ Database schema initialized successfully.")
