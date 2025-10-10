import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        # Establish connection to the MySQL database
        connection = mysql.connector.connect(
            host="127.0.0.1",       # Replace with your MySQL server host
            user="root",   # Replace with your MySQL username
            password="1234", # Replace with your MySQL password
            database="questify"  # Replace with your database name
        )

        if connection.is_connected():
            print("Connected to MySQL database")

            # Create a cursor object to execute SQL queries
            cursor = connection.cursor()

            # Example: Create a table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL
                )
            """)
            print("Table 'users' created or already exists.")

            # Example: Insert data into the table
            cursor.execute("""
                INSERT INTO users (name, email)
                VALUES (%s, %s)
            """, ("John Doe", "john.doe@example.com"))
            connection.commit()
            print("Data inserted successfully.")

            # Example: Retrieve data from the table
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            print("Retrieved data:")
            for row in rows:
                print(row)
        else :
            print(f"Something wrong")

    except Error as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    connect_to_database()
