from quixstreams import Application  # import the Quix Streams modules for interacting with Kafka:
# (see https://quix.io/docs/quix-streams/v2-0-latest/api-reference/quixstreams.html for more details)

# import additional modules as needed
import random
import os
import json
import logging
import csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Application()  # create an Application

# define the topic using the "output" environment variable
topic_name = os.environ["output"]
topic = app.topic(topic_name)


# this function loads the file and sends each row to the publisher
def get_data():
    """
    A function to read data from "sample.csv" and return it as a list of tuples with a message_key and rows
    """
    data_with_id = []
    message_key = f"MESSAGE_KEY_{str(random.randint(1, 100)).zfill(3)}"

    # Open the CSV file and read each row
    with open(os.environ["csv_file"], mode='r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            # Assuming each row is a dictionary, similar to the hardcoded data
            data_with_id.append((message_key, row))

    return data_with_id


def main():
    """
    Read data from the hardcoded dataset and publish it to Kafka
    """

    # create a pre-configured Producer object.
    producer = app.get_producer()

    with producer:
        # iterate over the data from the hardcoded dataset
        data_with_id = get_data()
        for message_key, row_data in data_with_id:

            json_data = json.dumps(row_data)  # convert the row to JSON

            # publish the data to the topic
            producer.produce(
                topic=topic.name,
                key=message_key,
                value=json_data,
            )
            logger.info(f"Published KEY: {message_key} | ROW: {json_data}")

        logger.info("All rows published")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Exiting.")