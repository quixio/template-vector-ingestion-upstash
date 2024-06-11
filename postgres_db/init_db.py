import psycopg2
import time

def create_table_and_insert():
    connection = None
    print("hello")
    for _ in range(5):  # Retry up to 5 times
        try:
            print('connecting...')
            connection = psycopg2.connect(
                user="root",
                password="root",
                host="db",
                port="5432",
                database="postgres"
            )
            cursor = connection.cursor()

            print('Connected')

            create_table_query = '''CREATE TABLE IF NOT EXISTS person (
                                    id SERIAL PRIMARY KEY,
                                    name VARCHAR(100) NOT NULL,
                                    age INT NOT NULL);'''
            cursor.execute(create_table_query)
            connection.commit()

            insert_query = '''INSERT INTO person (name, age) VALUES ('John Doe', 30);'''
            cursor.execute(insert_query)
            connection.commit()

            print("Table created and record inserted successfully")

            while True:
                print('running..')
                time.sleep(1)
            

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            time.sleep(5)  # Wait for 5 seconds before retrying

    if connection:
        print("closing connections")
        cursor.close()
        connection.close()

if __name__ == "__main__":
    print("starting")
    create_table_and_insert()