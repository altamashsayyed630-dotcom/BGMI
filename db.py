import mysql.connector
import os

def get_db_connection():
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        port=int(os.environ.get("DB_PORT", "10104")),
        ssl_disabled=False,
        database=os.environ.get("DB_NAME")
    )
    return conn