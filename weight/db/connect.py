import mysql.connector

try:
    # Update the connection with proper variable name 'cconn' and IP
    cconn = mysql.connector.connect(
        host="127.0.0.1",  # Use the correct IP or Docker host address
        port=5001,          # The mapped port for MySQL
        user="root",        # MySQL root user
        password="123",     # Replace with your actual root password
        database="weight"   # Database to connect to
    )

    print("Connection successful!")

    # Use the same variable name 'cconn' for the connection
    cursor = cconn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    print("Tables in the 'weight' database:")
    for table in tables:
        print(table)

    cursor.close()
    cconn.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")

