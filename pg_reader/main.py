from quixstreams import Application  # import the Quix Streams modules for interacting with Kafka:
# (see https://quix.io/docs/quix-streams/v2-0-latest/api-reference/quixstreams.html for more details)

# import additional modules as needed
import os
import json
import psycopg2
import time

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

print(os.environ)

user = os.getenv("pg_user", "")
pwd =  os.getenv("pg_pwd", "")
host =  os.getenv("pg_host", "")
port =  os.getenv("pg_port", "")
database =  os.getenv("pg_database", "")

app = Application(consumer_group="data_source", auto_create_topics=True)  # create an Application

# define the topic using the "output" environment variable
topic_name = os.environ["output"]
topic = app.topic(topic_name)


def read_from_db():
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

        read_query = '''SELECT * FROM person;'''
        cursor.execute(read_query)
        records = cursor.fetchall()

        print("Got records:")
        for row in records:
            print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

        print("Returning records")
        return records

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

def main():
    """
    Read data from the hardcoded dataset and publish it to Kafka
    """

    while True:
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        # not sure if this works but you get the idea..
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

        data_with_id = read_from_db()
        if data_with_id == None: 
            return

        with app.get_producer() as producer:
            for row_data in data_with_id:

                json_data = json.dumps(row_data)  # convert the row to JSON

                # publish the data to the topic
                producer.produce(
                    topic=topic.name,
                    key='POSTGRES_DATA',
                    value=json_data,
                )

                # for more help using QuixStreams see docs:
                # https://quix.io/docs/quix-streams/introduction.html

            print("All rows published")

            
        time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting.")