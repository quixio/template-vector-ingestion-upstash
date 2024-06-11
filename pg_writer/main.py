from quixstreams import Application
import os
import psycopg2
import time
import random

from dotenv import load_dotenv
load_dotenv()

user = os.getenv("pg_user", "")
pwd =  os.getenv("pg_pwd", "")
host =  os.getenv("pg_host", "")
port =  os.getenv("pg_port", "")
database =  os.getenv("pg_database", "")

def create_table():
    connection = None
    try:
        connection = psycopg2.connect(
            user=user,
            password=pwd,
            host=host,
            port=port,
            database=database
        )
        cursor = connection.cursor()

        create_table_query = '''CREATE TABLE IF NOT EXISTS person (
                                id SERIAL PRIMARY KEY,
                                name VARCHAR(100) NOT NULL,
                                age INT NOT NULL);'''
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created.")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        time.sleep(5)  # Wait for 5 seconds before retrying

    if connection:
        cursor.close()
        connection.close()

def insert_db_value():
    try:
        connection = psycopg2.connect(
            user=user,
            password=pwd,
            host=host,
            port=port,
            database=database
        )
        cursor = connection.cursor()

        print("Inserting data...")

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

# you decide what happens here!
def sink(message):
    value = message['mykey']

    # write value to DB from here..
    insert_db_value()


    # write_to_db(value) # implement your logic to write data or send alerts etc

    # for more help using QuixStreams see the docs:
    # https://quix.io/docs/quix-streams/introduction.html

app = Application(consumer_group="destination-v1", auto_offset_reset = "latest")

input_topic = app.topic(os.environ["input"])

sdf = app.dataframe(input_topic)

# call the sink function for every message received.
sdf = sdf.update(sink)

# you can print the data row if you want to see what's going on.
sdf = sdf.update(lambda row: print(row))

if __name__ == "__main__":
    create_table()
    app.run(sdf)
