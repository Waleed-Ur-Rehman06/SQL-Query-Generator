import sqlite3

def create_and_populate_db():
    """
    Creates and populates the student.db database with a STUDENT table.
    """
    try:
        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()

        # Drop the table if it already exists to ensure a clean start
        cursor.execute("DROP TABLE IF EXISTS STUDENT;")

        # Create the table with an additional MARKS column
        table_info = """
        CREATE TABLE STUDENT (
            NAME VARCHAR(25),
            CLASS VARCHAR(25),
            SECTION VARCHAR(25),
            MARKS INT
        );
        """
        cursor.execute(table_info)

        # Insert some records
        cursor.execute("INSERT INTO STUDENT VALUES ('waleed', 'Data Science', 'A', 92)")
        cursor.execute("INSERT INTO STUDENT VALUES ('hamza', 'Data Science', 'B', 100)")
        cursor.execute("INSERT INTO STUDENT VALUES ('zoha', 'Machine Learning', 'B', 84)")
        cursor.execute("INSERT INTO STUDENT VALUES ('zain', 'DevOps', 'A', 55)")
        cursor.execute("INSERT INTO STUDENT VALUES ('sarah', 'Machine Learning', 'A', 40)")

        connection.commit()
        print("Database 'student.db' created and populated successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    create_and_populate_db()
