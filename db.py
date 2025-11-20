import mysql.connector
from mysql.connector import Error
from config import Config

def get_db_connection():
    """
    Conexión simple a MySQL.
    Si algo se rompe, devolvemos None y lo manejamos en las vistas.
    """
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        return conn
    except Error as e:
        # En un proyecto real esto iría a logs
        print("Error conectando a MySQL:", e)
        return None
