from quixstreams import Application
from upstash_vector import Index

import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Application.Quix(
    "vectorizer",
    auto_offset_reset="earliest",
    auto_create_topics=True,  # Quix app has an option to auto create topics
)

# Define an input topic with JSON deserializer
input_topic = app.topic(os.environ['input'], value_deserializer="json") # Merlin.. i updated this for you

# Create collection to store items
index = Index(url=os.environ['upstash_vectordb_endpoint'], token=os.environ['upstash_vectordb_token'])

# Define the ingestion function
def ingest_vectors(row):

    index.upsert(
        vectors=[
            (row["id"], 
            row["embeddings"], 
               {"name": row["name"],
                "description": row["description"],
                "author": row["author"],
                "year": str(row["year"])}),
        ]
    )

    logger.info(f"Ingested vector entry id: '{row['id']}'...")

# Initialize a streaming dataframe based on the stream of messages from the input topic:
sdf = app.dataframe(topic=input_topic)

# INGESTION HAPPENS HERE
### Trigger the embedding function for any new messages(rows) detected in the filtered SDF
sdf = sdf.update(lambda row: ingest_vectors(row))
app.run(sdf)