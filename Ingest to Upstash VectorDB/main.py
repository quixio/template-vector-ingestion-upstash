from quixstreams import Application
from upstash_vector import Index
import os

encoder = SentenceTransformer('all-MiniLM-L6-v2') # Model to create embeddings
collection = os.environ['collectionname']

# Create collection to store items
index = Index(url=os.environ['upstash_vectordb_endpoint'], token=os.environ['upstash_vectordb_token'])

# Define the ingestion function
def ingest_vectors(row):

    index.upsert(
        vectors=[
            ("id1", row["embeddings"], {"metadata_field": "metadata_value"}),
        ]
    )

  print(f"Ingested vector entry id: '{row['id']}'...")

app = Application.Quix(
    "vectorizer",
    auto_offset_reset="earliest",
    auto_create_topics=True,  # Quix app has an option to auto create topics
)

# Define an input topic with JSON deserializer
input_topic = app.topic(os.environ['input'], value_deserializer="json") # Merlin.. i updated this for you

# Initialize a streaming dataframe based on the stream of messages from the input topic:
sdf = app.dataframe(topic=input_topic)

# INGESTION HAPPENS HERE
### Trigger the embedding function for any new messages(rows) detected in the filtered SDF
sdf = sdf.update(lambda row: ingest_vectors(row))
app.run(sdf)