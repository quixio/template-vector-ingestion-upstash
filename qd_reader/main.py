from quixstreams import Application  # import the Quix Streams modules for interacting with Kafka:
# (see https://quix.io/docs/quix-streams/v2-0-latest/api-reference/quixstreams.html for more details)

# import additional modules as needed
import os
import json
import requests
import time

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

host =  os.getenv("qd_host", "")
port =  os.getenv("qd_port", "")
collection =  os.getenv("qd_collection", "")

app = Application(consumer_group="data_source", auto_create_topics=True)  # create an Application

# define the topic using the "output" environment variable
topic_name = os.environ["output"]
topic = app.topic(topic_name)

def read_from_qdrant():
    url = f"http://{host}:{port}/collections"
    
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            print("Collections in Qdrant:")
            print(response.json())
        else:
            print(f"Failed to read from Qdrant: {response.status_code}")
        time.sleep(1)

def main():
    """
    Read data from the hardcoded dataset and publish it to Kafka
    """

    while True:
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        # not sure if this works but you get the idea..
        #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        with app.get_producer() as producer:
            # iterate over the data from the hardcoded dataset
            data_with_id = read_from_qdrant()
            for row_data in data_with_id:

                json_data = json.dumps(row_data)  # convert the row to JSON

                # publish the data to the topic
                producer.produce(
                    topic=topic.name,
                    key='QDRANT_DATA',
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