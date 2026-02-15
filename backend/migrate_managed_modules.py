import sqlite3
import os

db_path = 'aegis_one.db'
if not os.path.exists(db_path):
    print(f"Database {db_path} not found")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN managed_modules VARCHAR(500)")
        conn.commit()
        print("Column 'managed_modules' added successfully")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("Column 'managed_modules' already exists")
        else:
            print(f"Error: {e}")
    finally:
        conn.close()
