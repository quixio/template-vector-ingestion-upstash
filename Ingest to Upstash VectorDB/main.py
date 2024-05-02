from quixstreams import Application
from sentence_transformers import SentenceTransformer
from upstash_vector import Index
import os

encoder = SentenceTransformer('all-MiniLM-L6-v2') # Model to create embeddings
collection = os.environ['collectionname']

# Create collection to store items
index = Index(url="https://active-arachnid-42631-eu1-vector.upstash.io", token="********")

# Define the ingestion function
def ingest_vectors(row):

    # Creating a new dictionary that includes 'kind' and zips column names with values
    new_structure = {"kind": data["kind"]}
    new_structure.update({key: value for key, value in zip(data["columnnames"], data["columnvalues"])})

    # Optionally converting integers to strings
    new_structure["year"] = str(new_structure["year"])

    index.upsert(
        vectors=[
            ("id1", "Enter data as string", {"metadata_field": "metadata_value"}),
        ]
    )

  print(f'Ingested vector entry id: "{row["doc_uuid"]}"...')

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