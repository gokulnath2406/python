import mysql.connector
from mysql.connector import Error


def create_database_if_not_exists(database_name):
    try:
        # Connect to MySQL server without specifying a database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="g2000"
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
            password="g2000",
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
        name = input("enter new name ")
        role = input("enter new role ")
        salary = int(input("enter new salary "))

        # Insert data into the table
        sql = 'INSERT INTO employee (name, role, salary) VALUES (%s, %s, %s)'
        values = (name, role, salary)
        cursor.executemany(sql, [values])
        connection.commit()
        print('Data inserted successfully.')

    except Error as err:
        print(f"Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def update_database(database_var):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="g2000",
            database=database_var
        )
        cursor = connection.cursor()

        id_replace = int(input("enter ID "))
        new_name = input("enter new name ")
        new_role = input("enter new role ")
        new_salary = int(input("enter new salary "))

        sql = "UPDATE employee SET name = %s, role = %s, salary = %s WHERE emp_id = %s"
        val = (new_name, new_role, new_salary, id_replace)
        cursor.execute(sql, val)
        connection.commit()
        print(cursor.rowcount, "record(s) affected")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
def delete_id_database(database_var):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="g2000",
        database=database_var
    )
    cursor = connection.cursor()

    emp_id = int(input("enter ID "))
    sql = "DELETE FROM employee WHERE emp_id = %s"
    val = (emp_id,)
    cursor.execute(sql, val)
    connection.commit()
    print(f"{emp_id} is successfully deleted.")
    print(cursor.rowcount, "record(s) affected")
def duplicate_data_removal_database(database_var):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="g2000",
            database=database_var
        )
        cursor = connection.cursor()
        cursor.execute("""
                SELECT name, role, salary, MIN(emp_id) AS min_id
                FROM employee
                GROUP BY name, role, salary
                HAVING COUNT(*) > 1
            """)
        duplicate_groups = cursor.fetchall()
        for name, role, salary, min_id in duplicate_groups:
            cursor.execute("""
                    DELETE FROM employee
                    WHERE name = %s AND role = %s AND salary = %s AND emp_id != %s
                """, (name, role, salary, min_id))

        connection.commit()
        print("Duplicate records removed successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def create_elixir_table(database_var):
    try:
        # Connect to MySQL server without specifying a database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="g2000",
            database=database_var
        )
        cursor = connection.cursor()

        # Create the Elixir table with specified columns
        cursor.execute("""
                CREATE TABLE elixir (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50),
                    role VARCHAR(100),
                    salary INT
                )
            """)
        print("Elixir table created successfully.")

    except Error as err:
        print(f"Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
def update_data_from_employee_to_elixir(database_var):
    try:
        # Connect to MySQL server without specifying a database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="g2000",
            database=database_var
        )
        cursor = connection.cursor()
        # Select data from the employee table
        select_query = "SELECT * FROM employee"
        cursor.execute(select_query)
        employee_data = cursor.fetchall()

        # Insert data into the elixir table (adjust column names as needed)
        insert_query = "INSERT INTO elixir (name, role, salary) VALUES (%s, %s, %s)"

        for employee in employee_data:
            values = (employee[1], employee[2], employee[3])  # Replace with actual column indices
            print(values)
            cursor.execute(insert_query, values)

        # Commit changes
        connection.commit()

        print("Data transferred successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection regardless of exceptions
        if cursor:
            cursor.close()
        if connection:
            connection.close()
def logic_implementation_menu(database_var):
    print("\nWelcome to Employee Management Record")
    print("Press:")
    print("1 to Add Employee")
    print("2 to Remove Employee")
    print("3 to update Employee Details")
    print("4 to Display Employees")
    print("5 to Exit")

    menu_input = int(input("Enter your choice: "))
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="g2000",
            database=database_name
        )
        cursor = connection.cursor()
    except Error as err:
        print(f"Error: {err}")
        print("Please enter a valid database.")
    if menu_input == 1:
        create_table_and_insert_data(database_var)
    elif menu_input == 2:
        delete_id_database(database_var)
    elif menu_input == 3:
        update_database(database_var)
    elif menu_input == 4:
        select_query = "SELECT * FROM employee"
        cursor.execute(select_query)
        employee_data = cursor.fetchall()
        for i in employee_data:
            print(i)
    elif menu_input == 5:
        print("Thank you for using Employee Management Record!")
    else:
        print("Please provide valid input!")
        logic_implementation_menu(database_var)
    logic_implementation_menu(database_var)

#def add_Employee_using_menu(database_var, update_data_from_employee_to_elixir):

# Define your database name
database_var = 'emp'
database_name = 'emp'
# Create the database if it does not exist
#create_database_if_not_exists(database_var)
#create_table_and_insert_data(database_var)
#update_database(database_var)
#delete_id_database(database_var)
#duplicate_data_removal_database(database_var)
#create_elixir_table(database_var)
#update_data_from_employee_to_elixir(database_var)
print(logic_implementation_menu(database_var))