from quixstreams import Application
import os
import time
import json
import requests

from dotenv import load_dotenv
load_dotenv()

host =  os.getenv("qd_host", "")
port =  os.getenv("qd_port", "")
collection =  os.getenv("qd_collection", "")

def create_collection():
    url = f"http://{host}:{port}/collections/{collection}"
    headers = {"Content-Type": "application/json"}
    data = {
        "vectors": {
            "size": 3,
            "distance": "Cosine"
        }
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Collection created successfully")
    elif response.status_code == 409:
        print("Collection already exists")
    else:
        print(f"Failed to create collection: {response.status_code}")
        print(response.json())


def write_to_qdrant():
    url = f"http://{host}:{port}/collections/{collection}/points"
    headers = {"Content-Type": "application/json"}
    point_id = 1

    while True:
        data = {
            "points": [
                {
                    "id": point_id,
                    "vector": [0.1, 0.2, 0.3],
                    "payload": {"name": "John Doe", "age": 30}
                }
            ]
        }
        response = requests.put(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print(f"Successfully wrote point {point_id} to Qdrant")
        else:
            print(f"Failed to write to Qdrant: {response.status_code}")
            print(response.json())

        point_id += 1
        time.sleep(1)

# you decide what happens here!
def sink(message):
    value = message['mykey']

    # write value to DB from here..
    write_to_qdrant()


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
    create_collection()
    app.run(sdf)
