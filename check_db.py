# check_db.py
import sqlite3

conn = sqlite3.connect("trades.db")
cursor = conn.cursor()

print("\nOrders:")
for row in cursor.execute("SELECT * FROM orders"):
    print(row)

print("\nTrades:")
for row in cursor.execute("SELECT * FROM trades"):
    print(row)

conn.close()
