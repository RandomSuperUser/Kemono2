from flask import g, current_app
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from os import getenv

pool = None

def init():
    global pool
    try:
        pool = psycopg2.pool.ThreadedConnectionPool(1, 2000,
            host = getenv('PGHOST'),
            dbname = getenv('PGDATABASE'),
            user = getenv('PGUSER'),
            password = getenv('PGPASSWORD'),
            port = getenv('PGPORT') or 5432,
            cursor_factory = RealDictCursor
        )
    except Exception as error:
        print("Failed to connect to the database: ", error)
    return pool

def get_pool():
    return pool

def get_cursor():
    if 'cursor' not in g:
        g.connection = pool.getconn()
        g.cursor = g.connection.cursor()
    return g.cursor
