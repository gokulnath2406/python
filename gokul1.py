import mysql.connector
from mysql.connector import Error


def create_database_if_not_exists(database_name):
    try:
        # Connect to MySQL server without specifying a database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="qt008"
        )
        cursor = connection.cursor()

        # Create database if it does not exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"Database '{database_name}' is ready.")

    except Error as err:
        print(f"Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def create_table_and_insert_data(database_name):
    try:
        # Connect to the specific database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="qt008",
            database=database_name
        )
        cursor = connection.cursor()

        # Use the specified database
        cursor.execute(f"USE {database_name}")
        print("Database used.")

        # Create table if it does not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employee (
                emp_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50),
                role VARCHAR(100),
                salary INT
            )
        """)
        print("Table 'employee' created or already exists.")

        # Insert data into the table
        sql = 'INSERT INTO employee (name, role, salary) VALUES (%s, %s, %s)'
        values = [
            ('gokul', 'developer', 10000),
            ('mani', 'developer', 20000),
            ('bhakya', 'developer', 30000),
        ]
        cursor.executemany(sql, values)
        connection.commit()
        print('Data inserted successfully.')

    except Error as err:
        print(f"Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Define your database name
database_var = 'emp'

# Create the database if it does not exist
create_database_if_not_exists(database_var)

# Create the table and insert data
create_table_and_insert_data(database_var)
