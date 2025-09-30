import sqlite3

def connect_db(db_path):
    """Connect to SQLite DB."""
    conn = sqlite3.connect(db_path)
    return conn

def get_db_tables(conn):
    """Return list of table names."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [t[0] for t in cursor.fetchall()]

def get_table_rows(conn, table_name, limit=20, offset=0):
    """Return rows of a table."""
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit} OFFSET {offset};")
    return cursor.fetchall()

def get_table_columns(conn, table_name):
    """Return column names of a table."""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    return [col[1] for col in cursor.fetchall()]
