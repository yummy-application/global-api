import os

import mysql.connector
from load_dotenv import load_dotenv

load_dotenv()
db_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="my_pool",
    host="localhost",
    user="root",
    password=os.environ.get("DBPW"),
    database="yummy"
)

def get_connection():
    return db_pool.get_connection()

