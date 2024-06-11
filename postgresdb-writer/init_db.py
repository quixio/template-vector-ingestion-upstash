import psycopg2
import time
import random

def create_table_and_insert():
    connection = None
    while True:
        try:
            connection = psycopg2.connect(
                user="root",
                password="root",
                host="postgres",
                port="5432",
                database="test_db"
            )
            cursor = connection.cursor()

            create_table_query = '''CREATE TABLE IF NOT EXISTS person (
                                    id SERIAL PRIMARY KEY,
                                    name VARCHAR(100) NOT NULL,
                                    age INT NOT NULL);'''
            cursor.execute(create_table_query)
            connection.commit()
            print("Table created. Inserting data...")

            while True:
                random_age = random.randint(1, 100)
                insert_query = f'''INSERT INTO person (name, age) VALUES ('John Doe', {random_age});'''
                cursor.execute(insert_query)
                connection.commit()
                print(f"Inserted record with age: {random_age}")
                time.sleep(2)

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            time.sleep(5)  # Wait for 5 seconds before retrying

    if connection:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    create_table_and_insert()