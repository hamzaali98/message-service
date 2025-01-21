# test_connection.py
from app.db import engine

try:
    connection = engine.connect()
    print("Connection successful!")
    connection.close()
except Exception as e:
    print("Connection failed:", e)
