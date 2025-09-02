import sqlite3
import pandas as pd

def get_db_connection():
    """Establishes and returns a database connection."""
    return sqlite3.connect("student.db")

def get_table_schema(conn):
    """
    Dynamically retrieves the schema of all tables in the database.
    This is crucial for providing accurate context to the LLM.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_info = ""
    for table_name in tables:
        table_name = table_name[0]
        schema_info += f"Table: {table_name}\n"
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        column_info = [f"{col[1]} {col[2]}" for col in columns]
        schema_info += f"Columns: {', '.join(column_info)}\n\n"
        
    return schema_info

def execute_sql_query(sql_query, conn):
    """
    Executes a given SQL query and returns the results.
    Includes comprehensive error handling.
    """
    try:
        df = pd.read_sql_query(sql_query, conn)
        return df, None
    except pd.io.sql.DatabaseError as e:
        return None, str(e)
    finally:
        if conn:
            conn.close()