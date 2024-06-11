import requests
import time
import json


def create_collection():
    url = "http://qdrant:6333/collections/test_collection"
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
    url = "http://qdrant:6333/collections/test_collection/points"
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

if __name__ == "__main__":
    print("Creating collection..")
    create_collection()
    print("Collection created")
    print("Writing data..")
    write_to_qdrant()