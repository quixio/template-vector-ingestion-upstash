import psycopg2
import time

def read_from_db():
    try:
        connection = psycopg2.connect(
            user="root",
            password="root",
            host="postgres",
            port="5432",
            database="test_db"
        )
        cursor = connection.cursor()

        read_query = '''SELECT * FROM person;'''
        cursor.execute(read_query)
        records = cursor.fetchall()

        for row in records:
            print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    while True:
        read_from_db()
        time.sleep(1)