import mysql.connector
import os

def get_db_connection():
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST", "mysql-3caf8b47-altamashsayyed58-4d12.h.aivencloud.com"),
        user=os.environ.get("DB_USER", "avnadmin"),
        password=os.environ.get("DB_PASSWORD", "AVNS_1Rqp7MeILYuWMt3d3g2"),
        port=int(os.environ.get("DB_PORT", 10104)),
        ssl_disabled=False,
        database=os.environ.get("DB_NAME", "defaultdb")
    )
    return conn