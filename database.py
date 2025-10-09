import os
from dotenv import load_dotenv
import mysql.connector

# Cargar .env
load_dotenv()

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Error al conectar a MySQL: {e}")
        return None