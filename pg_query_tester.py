import psycopg2

db_params = {
    "host": "192.168.178.40",
    "database": "station_data",
    "user": "bahn_miner",
    "password": "bahn_miner_password",
    "port": "5432"
}

try:
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    query = "SELECT * FROM stations;"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)

except Exception as e:
    print(f"Error: {e}")

finally:
    if connection:
        cursor.close()
        connection.close()
        print("Connection closed.")
