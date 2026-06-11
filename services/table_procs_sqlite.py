import sqlite3

_conn = None

def open_sqlite_conn(database_file):
    global _conn
    _conn = sqlite3.connect(database_file)

def close_sqlite_conn():
    global _conn
    if _conn:
        _conn.close()

def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def list_all_tables(database_file):
    """
    Connects to an SQLite database and lists all table names.
    Args:
        database_file (str): The path to the SQLite database file.
    Returns:
        list: A list of table names (excluding internal sqlite_ sequence/stat tables).
    """
    global _conn
    try:
        # conn = sqlite3.connect(database_file)
        cursor = _conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables if not table[0].startswith('sqlite_')]
        return table_names
    except sqlite3.Error as e:
        print(f"A database error occurred: {e}")
        return []
    # finally:
    #     if _conn:
    #         _conn.close()

def get_table_info(table_name):
    """
    Retrieves detailed information about columns in a specific table using PRAGMA.
    """
    _conn.row_factory = dict_factory
    #_conn.row_factory = sqlite3.Row
    cursor = _conn.cursor()
    # Note: PRAGMA statements do not work with parameterized queries, so use f-strings carefully
    # and ensure table_name is a trusted source.
    # cursor.execute(f"PRAGMA table_info('{table_name}');")
    cursor.execute(f"SELECT * FROM pragma_table_info('{table_name}')")
    columns_info = cursor.fetchall()
    return columns_info