# db_config.py
from dotenv import load_dotenv
import os
load_dotenv()

DB = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "MySQL@123"),
    "database": os.getenv("DB_NAME", "hotel_booking"),
    "port": int(os.getenv("DB_PORT", 3306))
}
