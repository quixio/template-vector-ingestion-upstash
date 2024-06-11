import requests
import time 


def read_from_qdrant():
    url = "http://qdrant:6333/collections"
    
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            print("Collections in Qdrant:")
            print(response.json())
        else:
            print(f"Failed to read from Qdrant: {response.status_code}")
        time.sleep(1)

if __name__ == "__main__":
    read_from_qdrant()