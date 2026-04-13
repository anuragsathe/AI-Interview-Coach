from database.models import init_db
import sys

try:
    print("Attempting to initialize database...")
    init_db()
    print("Database initialization successful!")
except Exception as e:
    print(f"DATABASE ERROR DETECTED: {e}")
    sys.exit(1)
